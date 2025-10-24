# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

# signals.py
"""
Anaconda Telemetry - Metrics Module

This module provides functionality for logging, metrics, and tracing (together called
signals) using OpenTelemetry. It includes classes for handling logging, metrics, and
tracing, as well as functions for initializing the telemetry system and recording metrics.
"""

import logging, hashlib, re, socket, json
from abc import ABC
from typing import Dict, Iterator, Any, List, Union, Sequence, Optional
from contextlib import contextmanager
from dataclasses import fields

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider, Counter, UpDownCounter, Histogram, ObservableCounter, ObservableUpDownCounter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter, AggregationTemporality
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.propagate import get_global_textmap
from opentelemetry.trace.status import StatusCode

from .config import Configuration as Config
from .exporters import OTLPExporterShim
from .attributes import ResourceAttributes as Attributes
from .__version__ import __SDK_VERSION__, __TELEMETRY_SCHEMA_VERSION__

# Limited Dict for attributes in OTel
Scalar = Union[str, bool, int, float]
AttrDict = Dict[str, Union[str, bool, int, float, Sequence[Scalar]]]


class MetricsNotInitialized(RuntimeError):
    pass


class _AnacondaCommon:
    # Base class for common attributes and methods (internal only)
    def __init__(self, config: Config, attributes: Attributes):
        self._config = config
        # Init resource_attributes
        self._resource_attributes = {}
        self.resource = None
        # session id
        self._session_id = None

        # Make self._resource_attributes and self.resource
        self.make_otel_resource(attributes)

        self.logger = logging.getLogger(__package__)

        # assemble config and attribute values
        # default endpoint
        self.default_endpoint = config._get_default_endpoint()
        # export options
        self.use_console_exporters = config._get_console_exporter()

    def make_otel_resource(self, attributes: Attributes):
        # Read resource attributes
        resource_attrs = attributes._get_attributes()
        # Required parameters
        self.service_name = resource_attrs["service_name"]
        self.service_version = resource_attrs["service_version"]
        del resource_attrs["service_name"], resource_attrs["service_version"]
        # convert parameters value to stringified JSON
        resource_attrs["parameters"] = json.dumps(resource_attrs["parameters"])
        # Init resource_attributes
        self._resource_attributes = {
                SERVICE_NAME: self.service_name,
                SERVICE_VERSION: self.service_version
        }
        self._resource_attributes.update(resource_attrs)
        # convert to otel names
        for attr in fields(attributes):
            otel_name = attr.metadata.get('otel_name', None)
            if otel_name:
                self._resource_attributes[attr.metadata['otel_name']] = self._resource_attributes.pop(attr.name)
        self._session_id = self._hash_session_id(self._config._get_tracing_session_entropy())
        self._resource_attributes['session.id'] = self._session_id
        self.resource = Resource.create(self._resource_attributes)


    def _hash_session_id(self, entropy):
        # Hashes a session id for common attributes based on timestamp and user_id
        # entropy value ensures unique session_ids
        if entropy is None:
            raise KeyError("The entropy key has been removed.")

        user_id = self._resource_attributes.get('user.id', '')
        combined = f"{entropy}|{user_id}|{self.service_name}"
        hashed = hashlib.sha256(combined.encode("utf-8")).hexdigest()

        return hashed


class _AnacondaLogger(_AnacondaCommon):
    # Singleton instance (internal only); provide a logger handler for OpenTelemetry log instrumentation
    _instance = None

    def __init__(self, config: Config, attributes: Attributes):
        super().__init__(config, attributes)
        self.log_level = self._get_log_level(config._get_logging_level())
        self.logger_endpoint = config._get_logging_endpoint()

        # Create logger provider
        self._provider = LoggerProvider(resource=self.resource)
        self._console_exporter: ConsoleLogExporter | None = None
        # Add OTLP exporter
        if self.use_console_exporters:
            exporter = ConsoleLogExporter()
            self._console_exporter = exporter
        else:
            auth_token = config._get_auth_token_logging()
            headers: Dict[str, str] = {}
            if auth_token is not None:
                headers['authorization'] = f'Bearer {auth_token}'
            if config._get_request_protocol_logging() in ['grpc', 'grpcs']:  # gRPC
                from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter as OTLPLogExportergRPC
                insecure = not config._get_TLS_logging()
                exporter = OTLPLogExportergRPC(endpoint=self.logger_endpoint,
                                        insecure=insecure,
                                        credentials=config._get_ca_cert_logging() if not insecure else None,
                                        headers=headers)
            else:  # HTTP
                from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter as OTLPLogExporterHTTP
                exporter = OTLPLogExporterHTTP(endpoint=self.logger_endpoint,
                                        certificate_file=config._get_ca_cert_logging(),
                                        headers=headers)
        self._exporter = exporter
        self._processor = BatchLogRecordProcessor(self._exporter)
        self._provider.add_log_record_processor(self._processor)
        self._handler = LoggingHandler(level=self.log_level, logger_provider=self._provider)

    def tear_down(self):
        _AnacondaLogger._instance = None

    def _get_log_level(self, str_level: str)-> int:
        # Convert string from config file to logging level.
        levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "warn": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
            "fatal": logging.CRITICAL
        }
        return levels.get(str_level.lower(), logging.DEBUG)

    def _test_set_console_mock(self, new_out):  # For testing only...
        if self._console_exporter is not None and new_out is not None:
            saved = self._console_exporter.out
            self._console_exporter.out = new_out
            return saved
        return None


class _AnacondaMetrics(_AnacondaCommon):
    # Singleton instance (internal only); provide a single instance of the metrics class
    _instance = None

    _default_temporality: dict[type,AggregationTemporality] = {
        Counter: AggregationTemporality.DELTA,
        ObservableCounter: AggregationTemporality.DELTA,
        Histogram: AggregationTemporality.DELTA,
        UpDownCounter: AggregationTemporality.CUMULATIVE,
        ObservableUpDownCounter: AggregationTemporality.CUMULATIVE,
    }

    _cumulative_temporality: dict[type,AggregationTemporality] = {
        Counter: AggregationTemporality.CUMULATIVE,
        ObservableCounter: AggregationTemporality.CUMULATIVE,
        Histogram: AggregationTemporality.CUMULATIVE,
        UpDownCounter: AggregationTemporality.CUMULATIVE,
        ObservableUpDownCounter: AggregationTemporality.CUMULATIVE,
    }

    _temporalityValue: dict[bool,str] = {
        False: "DELTA",
        True: "CUMULATIVE"
    }

    def __init__(self, config: Config, attributes: Attributes):
        super().__init__(config, attributes)

        self.metrics_endpoint = config._get_metrics_endpoint()
        self.telemetry_export_interval_millis = config._get_metrics_export_interval_ms()
        self.counter_objects: Dict[str, Any] = {}
        self.up_down_counter_objects: Dict[str, Any] = {}
        self.histogram_objects: Dict[str, Any] = {}

        self.meter = self._setup_metrics(config)
        self.create_dispatcher = {
            'simple_counter': self.meter.create_counter,
            'simple_up_down_counter': self.meter.create_up_down_counter,
            'histogram': self.meter.create_histogram
        }
        self.type_list = {
            'simple_counter': self.counter_objects,
            'simple_up_down_counter': self.up_down_counter_objects,
            'histogram': self.histogram_objects
        }
        self.metric_reader: PeriodicExportingMetricReader = None

    def tear_down(self):
        if self.metric_reader is not None:
            self.metric_reader.force_flush()
            self.metric_reader.shutdown()
            self.metric_reader = None

        _AnacondaMetrics._instance = None

    def _setup_metrics(self, config: Config) -> metrics.Meter:
        if self.use_console_exporters:
            exporter = ConsoleMetricExporter(preferred_temporality=self._get_temporality())
            self.exporter_shim = None
        else:
            auth_token = config._get_auth_token_metrics()
            headers: Dict[str, str] = {}
            if auth_token is not None:
                headers['authorization'] = f'Bearer {auth_token}'
            if config._get_request_protocol_metrics() in ['grpc', 'grpcs']:  # gRPC
                from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter as OTLPMetricExportergRPC
                insecure = not config._get_TLS_metrics()
                exporter = OTLPMetricExportergRPC(endpoint=self.metrics_endpoint,
                                        insecure=insecure,
                                        credentials=config._get_ca_cert_metrics() if not insecure else None,
                                        headers=headers,
                                        preferred_temporality=self._get_temporality())
            else:  # HTTP
                from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter as OTLPMetricExporterHTTP
                self.exporter_shim = OTLPExporterShim(
                    OTLPMetricExporterHTTP,
                    endpoint=self.metrics_endpoint,
                    certificate_file=config._get_ca_cert_metrics(),
                    headers=headers,
                    preferred_temporality=self._get_temporality()
                )
                exporter = self.exporter_shim

        self.exporter = exporter
        self.metric_reader = PeriodicExportingMetricReader(self.exporter, export_interval_millis=self.telemetry_export_interval_millis)

        # Create and set meter provider
        meter_provider = MeterProvider(
            resource=self.resource,
            metric_readers=[self.metric_reader]
        )
        try:
            metrics.set_meter_provider(meter_provider)
        except Exception as e:
            self.logger.warning(f"The metrics provider was previously set and will take precidence over this call.")
        # Get meter for this service
        return metrics.get_meter(self.service_name, self.service_version)

    def _get_temporality(self) -> dict[type,AggregationTemporality]:
        if self._config._get_use_cumulative_metrics() == True:
            return _AnacondaMetrics._cumulative_temporality
        return _AnacondaMetrics._default_temporality

    def _check_for_metric(self, metric_name: str, metric_type: str) -> bool:
        bucket_list = self.type_list.get(metric_type, None)
        if bucket_list is None:
            return False
        return bucket_list.get(metric_name, None) is not None

    def _get_or_create_metric(self, metric_name: str, metric_type: str = 'simple_up_down_counter', units: str = '#', description='No description.') -> Any:
        bucket_list = self.type_list.get(metric_type, None)
        if bucket_list is None:
            raise MetricsNotInitialized(f"Metric type '{metric_type}' is unknown!")
        metric = bucket_list.get(metric_name, None)
        if metric is None:
            if not re.fullmatch(r"^[A-Za-z][A-Za-z_0-9]+$", metric_name):
                self.logger.warning(f"Metric {metric_name} does not match valid regex: r\"^[A-Za-z][A-Za-z_0-9]+$\"")
                return None
            create = self.create_dispatcher.get(metric_type, None)
            if create is None:
                self.logger.warning(f"Metric '{metric_name}' has an invalid type '{metric_type}'; cannot create metric.")
                return None
            metric = create(
                metric_name,
                unit=units,
                description=description
            )
            if metric is None:
                self.logger.error(f"Failed to create metric '{metric_name}'!")
            bucket_list[metric_name] = metric
        return metric

    def record_histogram(self, metric_name, value, attributes: AttrDict={}) -> bool:
        # Record a histogram metric with the given name and value.
        metric = self._get_or_create_metric(metric_name, metric_type='histogram', units='#', description='Dynamically create histogram metric.')
        if metric is None:
            self.logger.error(f"Metric '{metric_name}' failed to be created.")
            return False
        metric.record(value, attributes)
        return True

    def increment_counter(self, counter_name, by=1, attributes: AttrDict={}) -> bool:
        # Increment a counter with the given name by the 'by' parameter. abs(by) is used.
        metric = None
        if self._check_for_metric(metric_name=counter_name, metric_type='simple_counter'):
            metric = self._get_or_create_metric(counter_name, metric_type='simple_counter')
        if metric is None:
            metric = self._get_or_create_metric(counter_name, metric_type='simple_up_down_counter')
        if metric is None:
            self.logger.error(f"Metric '{counter_name}' failed to be created.")
            return False
        metric.add(abs(by), attributes)
        return True

    def decrement_counter(self, counter_name, by=1, attributes:AttrDict={}) -> bool:
        # Decrement a up down counter with the given name by the 'by' parameter. abs(by) is used.
        metric = self._get_or_create_metric(counter_name)
        if metric is None:
            self.logger.error(f"Metric '{counter_name}' failed to be created.")
            return False
        metric.add(-abs(by), attributes)
        return True


class ASpan(ABC):
    """
    Abstract base class for a span in the tracing system. This class should not be instantiated directly.
    Use the get_trace function to create an instance of this class.
    """
    def add_event(self, name: str, attributes: AttrDict = None) -> None:
        """
        Add an event to the span with the given name and attributes.

        Args:
            name (str): The name of the event.
            attributes (dict, optional): Additional attributes for the event. Defaults to None.
        """
        pass

    def add_exception(self, exception: Exception) -> None:
        """
        Add an exception to the span. If the exception is None, a generic exception is recorded.

        Args:
            exception (Exception): The exception to add to the span.
        """
        pass

    def set_error_status(self, msg: Optional[str] = None) -> None:
        """
        Set the status of the span to ERROR. This indicates that an error occurred during the span's execution.

        Args:
            msg (str, optional): An optional message to include in the error status. Defaults to None.
        """
        pass

    def add_attributes(self, attributes: AttrDict) -> None:
        """
        Adds attributes for the span (adds to the orginal attribute on creation of the span).

        Args:
            attributes (dict): A dictionary of attributes to add for the span.
        """
        pass


class _ASpan(ASpan):
    # A single class for the tracing yielded return value.
    def __init__(self, name: str, span: trace.Span, attributes: AttrDict = {}, noop: bool = False) -> None:
        self._noop = noop
        self._name = name
        self._attributes: AttrDict = attributes
        self._span: trace.Span = span

    def add_event(self, name: str, attributes: AttrDict = None) -> None:
        if self._noop: return
        if attributes is None:
            attributes = {}
        self._span.add_event(f"{self._name}.{name}", attributes=attributes)

    def add_exception(self, exception: Exception) -> None:
        if self._noop: return
        if exception is None:
            exception = Exception("Generic exception because the exception passed was None.")

        self._span.record_exception(exception,
                                    attributes={
                                        "exception.type": type(exception).__name__,
                                        "exception.message": str(exception)
                                    })

    def set_error_status(self, msg: Optional[str] = None) -> None:
        if self._noop: return
        self._span.set_status(StatusCode.ERROR, msg if msg else "An error occurred during the span's execution.")

    def add_attributes(self, attributes: AttrDict) -> None:
        if self._noop: return
        if not isinstance(attributes, dict):
            raise TypeError("Attributes must be a dictionary of string key and string values.")
        self._attributes.update(attributes)
        self._span.set_attributes(self._attributes)

    def _close(self) -> None:
        if self._noop: return
        self._span.end()


class _AnacondaTrace(_AnacondaCommon):
    # Singleton instance (internal only); provide a single instance of the tracing class
    _instance = None

    def __init__(self, config: Config, attributes: Attributes):
        # Init singleton instance
        super().__init__(config, attributes)
        self.tracing_endpoint = config._get_tracing_endpoint()

        self.tracer = self._setup_tracing(config)

    def tear_down(self):
        # TODO: flush and shutdown
        _AnacondaTrace._instance = None

    def _setup_tracing(self, config: Config) -> trace.Tracer:
        # Create tracer provider
        tracer_provider = TracerProvider(resource=self.resource)

        # Add OTLP exporter
        if self.use_console_exporters:
            exporter = ConsoleSpanExporter()
        else:
            auth_token = config._get_auth_token_tracing()
            headers: Dict[str, str] = {}
            if auth_token is not None:
                headers['authorization'] = f'Bearer {auth_token}'
            if config._get_request_protocol_tracing() in ['grpc', 'grpcs']:  # gRPC
                insecure = not config._get_TLS_tracing()
                from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as OTLPSpanExportergRPC
                exporter = OTLPSpanExportergRPC(endpoint=self.tracing_endpoint,
                                        insecure=insecure,
                                        credentials=config._get_ca_cert_tracing() if not insecure else None,
                                        headers=headers)
            else:  # HTTP
                from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as OTLPSpanExporterHTTP
                exporter = OTLPSpanExporterHTTP(endpoint=self.tracing_endpoint,
                                        certificate_file=config._get_ca_cert_tracing(),
                                        headers=headers)
        tracer_provider.add_span_processor(
            BatchSpanProcessor(exporter)
        )

        # Set as global provider
        try:
            trace.set_tracer_provider(tracer_provider)
        except Exception:
            self.logger.warning(f"The tracer provider was previously set, and will take precidence over the set in this package: anaconda_opentelemetry.")

        # Get tracer for this service
        return trace.get_tracer(self.service_name, self.service_version)

    def get_span(self, name: str, attributes: AttrDict = {}, carrier: Dict[str,str] = None) -> trace.Span:
        # Get a span with the given name and attributes.
        if carrier is None:
            context = None
        else:
            context = get_global_textmap().extract(carrier)
        span = self.tracer.start_span(name, context=context, attributes=attributes)
        return _ASpan(name, span, attributes=attributes)


# Internet and endpoint access check method
def __check_internet_status(config: Config, timeout: float = 5.0) -> tuple[bool,bool]: # seconds max to pause....
    # Relies on Configuration to validate the endpoint...
    internet = True
    access = True
    if config._get_skip_internet_check():
        return True, True
    endpoint = config._get_default_endpoint()
    try:
        # Access to a highly available DNS site...
        socket.create_connection(('8.8.8.8', 53), timeout=timeout / 2).close()
    except OSError:
        logging.getLogger(__package__).warning("Anaconda OpenTelemetry: No Internet was detected!")
        internet = False  # No internet, but internet is not an absolute requirement for on-prem solutions.
    try:
        socket.create_connection((config._endpoints['default_endpoint'].host, config._endpoints['default_endpoint']._internet_check_port), timeout=timeout / 2).close()
    except OSError:
        logging.getLogger(__package__).fatal(f"Anaconda OpenTelemetry: No access to the endpoint '{endpoint}'!")
        access = False # This could be fatal, not endpoint for telemetry.
    if access == True:
        logging.getLogger(__package__).info(f"Anaconda OpenTelemetry: Successful access to the endpoint '{endpoint}'!")
    return internet, access

__ANACONDA_TELEMETRY_INITIALIZED = False
__SIGNALS = None
__CONFIG = None

def _is_first_time():  # For testing only.
    global __ANACONDA_TELEMETRY_INITIALIZED
    global __SIGNALS
    global __CONFIG
    return __ANACONDA_TELEMETRY_INITIALIZED == False and (__CONFIG is None or __SIGNALS is None)

################################################################################
# Exposed APIs
def initialize_telemetry(config: Config,
                         attributes: Attributes = None,
                         signal_types: List[str] = ['metrics']):  # Follows what the backend has implemented.
    """
    Initializes the telemetry system.

    Args:
        service_name (str): The name of the service.
        service_version (str): The version of the service.
        config (Configuration): The configuration for the telemetry. At a minimum, the Configuration must have a default endpoint
            for connection to the collector.
        attributes (ResourceAttributes, optional): A class containing common attributes. If provided,
            it will override any values shared with configuration file.
        signal_types (list, optional): List of metric types to initialize. Defaults to ['logging','metrics','tracing'].
            Supported values are 'logging', 'metrics', and 'tracing'. If an empty list is provided, no metrics will be initialized.

    Raises:
        ValueError: If the config passed is None or the attributes passed are None.
    """
    global __ANACONDA_TELEMETRY_INITIALIZED
    global __SIGNALS
    global __CONFIG

    if __ANACONDA_TELEMETRY_INITIALIZED is True:
        return  # Already initialized
    if config is None:
        raise ValueError(f"The config argument is required but was None")
    if attributes is None:
        raise ValueError(f"The attributes argument is required but was None")

    __CONFIG = config
    __SIGNALS = signal_types

    re_initialize_telemetry(attributes)

def update_endpoint(signal: str, new_endpoint: str):
    # no signal param usage yet
    updated_endpoint = _AnacondaMetrics._instance.exporter.update_endpoint(
        _AnacondaMetrics._instance._config,
        new_endpoint
    )

    if not updated_endpoint:
        logging.getLogger(__package__).warning(f"Endpoint for {signal} failed to update.")
        return False
    else:
        logging.getLogger(__package__).info(f"Endpoint for {signal} was successfully updated.")
    return True

def re_initialize_telemetry(attributes: Attributes):
    """
    Re-intialize the telemetry with new attributes. The configuration and signal types are identical
    to the original initialize_telemetry() call.

    Args:
        attributes (ResourceAttributes, optional): A class containing common attributes. If provided,
            it will override any values shared with configuration file.

    Raises:
        ValueError: If the attributes passed are None. Will throw exceptions
        if initialize_telemetry has not been previously run.
    """
    global __ANACONDA_TELEMETRY_INITIALIZED
    global __SIGNALS
    global __CONFIG

    if _is_first_time():
        raise RuntimeError("re_initialize_telemetry called without first calling initialize_telemetry first!")

    if __ANACONDA_TELEMETRY_INITIALIZED:
        if 'metrics' in __SIGNALS and _AnacondaMetrics._instance is not None:
            _AnacondaMetrics._instance.tear_down()
        if 'tracing' in __SIGNALS and _AnacondaTrace._instance is not None:
            _AnacondaTrace._instance.tear_down()
        if 'logging' in __SIGNALS and _AnacondaLogger._instance is not None:
            _AnacondaLogger._instance.tear_down()

        __ANACONDA_TELEMETRY_INITIALIZED = False

    config = __CONFIG
    signal_types = __SIGNALS

    # Check ResourceAttributes object
    if attributes is None:
        raise ValueError(f"The attributes argument is required but was None")
    elif type(attributes.parameters) != dict:
        raise ValueError(f"The parameters attribute in ResourceAttributes must be a dictionary")

    # Right now, no acction is taken but it possible to disable telemetry with no access to the endpoint...
    _, _ = __check_internet_status(config, timeout=4)  # Max wait 4 seconds...

    # all params are the same currently so only write them once
    init_params = (config, attributes)

    # Initialize logging here...
    signal_type_count = 0
    if 'logging' in signal_types:
        _AnacondaLogger._instance = _AnacondaLogger(*init_params)
        signal_type_count += 1

    # Initialize the telemetry system here
    if 'metrics' in signal_types:
        _AnacondaMetrics._instance = _AnacondaMetrics(*init_params)
        signal_type_count += 1

    # Initialize tracing here...
    if 'tracing' in signal_types:
        _AnacondaTrace._instance = _AnacondaTrace(*init_params)
        signal_type_count += 1

    if signal_type_count == 0:
        logging.getLogger(__package__).warning(
            "No signal types were initialized. Was this intended? If not please check the " +
              "'metrics' section in the configuration file and/or the list of " +
              "metric types in the parameter 'signal_types'."
        )
    __ANACONDA_TELEMETRY_INITIALIZED = True

def record_histogram(metric_name, value, attributes: AttrDict={}) -> bool:
    """
    Records a increasing only metric with the given name and value. The value will
    always appear in the attributes section in the raw OTLP output and the timestamp
    will be the histogram value.

    Will catch any exceptions generated by metric usage.

    Args:
        metric_name (str): The name of the metric.
        value (float): The value of the metric. Can be any float since the timestamp is the ever increasing value of the histogram.
        attributes (dict, optional): Additional attributes for the metric. Defaults to {}.

    Returns:
        bool: True if the metric was recorded successfully, False otherwise (logging the error).
    """
    if __ANACONDA_TELEMETRY_INITIALIZED is False:
        logging.getLogger(__package__).error("Anaconda telemetry system not initialized.")  # Since init didn't happen this is not exported in OTel!!!
        return False
    try:
        return _AnacondaMetrics._instance.record_histogram(metric_name, value, attributes)
    except MetricsNotInitialized as me:
        logging.getLogger(__package__).warning(f"An attempt was made to record a histogram metric when metrics were not configured.")
        return False
    except Exception as e:
        logging.getLogger(__package__).error(f"UNCAUGHT EXCEPTION:\n{e}")
        return False

def increment_counter(counter_name, by=1, attributes: AttrDict={}) -> bool:
    """
    Increments a counter or up down counter by the given parameter 'by'.

    Will catch any exceptions generated by metric usage.

    Args:
        counter_name (str): The name of the counter.
        by (int, optional): The value to increment by. Defaults to 1. The abs(by) is used to protect from negative numbers.
        attributes (dict, optional): Additional attributes for the counter. Defaults to {}.

    Returns:
        bool: True if the counter was incremented successfully, False otherwise (logging the error).
    """
    if __ANACONDA_TELEMETRY_INITIALIZED is False:
        logging.getLogger(__package__).error("Anaconda telemetry system not initialized.")  # Since init didn't happen this is not exported in OTel!!!
        return False
    try:
        return _AnacondaMetrics._instance.increment_counter(counter_name, by, attributes)
    except MetricsNotInitialized as me:
        logging.getLogger(__package__).warning(f"An attempt was made to change/create a counter metric when metrics were not configured.")
        return False
    except Exception as e:
        logging.getLogger(__package__).error(f"UNCAUGHT EXCEPTION:\n{e}")
        return False

def decrement_counter(counter_name, by=1, attributes: AttrDict={}) -> bool:
    """
    Decrements a up down counter with the given name and value. If applied to a regular counter it will log a warning and silently fail.

    Will catch any exceptions generated by metric usage.

    Args:
        counter_name (str): The name of the counter.
        by (int, optional): The value to decrement by. Defaults to 1. abs(by) is used to protect from negative numbers.
        attributes (dict, optional): Additional attributes for the counter. Defaults to {}.

    Returns:
        bool: True if the counter was decremented successfully, False otherwise (logging the error).
    """
    if __ANACONDA_TELEMETRY_INITIALIZED is False:
        logging.getLogger(__package__).error("Anaconda telemetry system not initialized.")  # Since init didn't happen this is not exported in OTel!!!
        return False
    try:
        return _AnacondaMetrics._instance.decrement_counter(counter_name, by, attributes)
    except MetricsNotInitialized as me:
        logging.getLogger(__package__).warning(f"An attempt was made to change/create a counter metric when metrics were not configured.")
        return False
    except Exception as e:
        logging.getLogger(__package__).error(f"UNCAUGHT EXCEPTION:\n{e}")
        return False

@contextmanager
def get_trace(name: str, attributes: AttrDict = {}, carrier: Dict[str,str] = None) -> Iterator[_ASpan]:
    """
    Create or continue a named trace (based on the 'carrier' parameter).

    Use the function like a Python I/O object (keyword 'with') to ensure the span is closed properly.

    Will catch any exceptions generated by tracing usage.

    Args:
        name (str): The name of the trace.
        attributes (dict, optional): Additional attributes for the trace.  Defaults to {}.
        carrier (dict, optional): The carrier used to continue a trace context in the output data. Defaults to None.

    Example:
        with get_trace("my_trace_name", {"key": "value"}) as span:
            # Do some work here
            pass
            # The span will be closed automatically when exiting the 'with' block.

    Returns:
        Iterator[Tracer]: An iterator for the tracer.
    """
    if __ANACONDA_TELEMETRY_INITIALIZED is False:
        logging.getLogger(__package__).error("Anaconda telemetry system not initialized.")  # Since init didn't happen this is not exported in OTel!!!
        return None

    # check attributes for invalid keys
    if any(not isinstance(key, str) or not key for key in attributes):
        logging.getLogger(__package__).error("Attribute passed with non empty str type key. Invalid attributes.")

    try:
        aspan = _AnacondaTrace._instance.get_span(name, attributes, carrier)
    except:  # Trace is different than the other signals, there is no easy way to log and continue.
        logging.getLogger(__package__).warning(f"Attempt to trace a with-block when tracing was not configured.")
        aspan = _ASpan("UNKNOWN", span=None, noop=True)
    try:
        yield aspan
    except Exception as e:
        aspan.add_exception(e)
        aspan.set_error_status()
        _AnacondaTrace._instance.logger.error(f"Error in trace span {name}: {e}")
    finally:
        aspan._close()

def get_telemetry_logger_handler() -> LoggingHandler:
    """
    Returns the telemetry logger handler. This lets the package user control how the application uses the telemetry logger.
    Insert this handler into your named logger.

        log = logging.getLogger("my_logger")
        log.addHandler(get_telemetry_logger_handler())

    Previously, this was injected into the root logger, but this turned out to be problematic for some applications that
    wanted to control the logging configuration more precisely. This injection behavior is now disabled. If you wish to
    inject the handler into the root logger, you can do so manually. See the Python logging documentation for more information.

    Returns:
        logging.Logger: The telemetry logger handler if logging was enabled via signal_types in initialize_telemetry,
        otherwise this function returns None.
    Raises:
        RuntimeError: if `initialize_telemetry` has not been called
    """
    global __ANACONDA_TELEMETRY_INITIALIZED
    if __ANACONDA_TELEMETRY_INITIALIZED is False:
        logging.getLogger(__package__).error("Anaconda telemetry system not initialized.")  # Since init didn't happen this is not exported in OTel!!!
        raise RuntimeError("Anaconda telemetry system not initialized.")
    if _AnacondaLogger._instance is not None:
        return _AnacondaLogger._instance._handler
    return None  # No logger handler available, logging not initialized or not configured.
