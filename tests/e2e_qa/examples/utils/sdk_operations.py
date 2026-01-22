# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
SDK Operations with Integrated Logging

This module provides wrapper functions for SDK operations that include
integrated detailed logging. This keeps example code clean and concise
while still providing comprehensive logging when USE_DETAILED_LOG=true.

Usage:
    from utils.sdk_operations import SdkOperations
    
    sdk = SdkOperations(endpoint="http://localhost:4318")
    
    # Create configuration with logging
    config = sdk.create_configuration(endpoint="http://localhost:4318")
    
    # Create attributes with logging
    attrs = sdk.create_attributes(service_name="my-service", service_version="1.0.0")
    
    # Set custom attributes with logging
    sdk.set_custom_attributes(attrs, team="data-science", region="us-east")
    
    # Initialize telemetry with logging
    sdk.initialize(config, attrs, signal_types=['metrics'])
    
    # Increment counter with logging
    sdk.increment_counter("api_requests_total", by=100, 
                         attributes={"http.method": "GET"})
    
    # Record histogram with logging
    sdk.record_histogram("request_duration_ms", 45.0,
                        attributes={"region": "us-east"})
"""

import logging
import time
from typing import Any, Dict, List, Optional, Union
from opentelemetry import metrics, trace
from anaconda.opentelemetry import (
    Configuration,
    ResourceAttributes,
    initialize_telemetry,
    increment_counter,
    decrement_counter,
    record_histogram,
    get_trace,
)
from anaconda.opentelemetry.signals import _AnacondaLogger, get_telemetry_logger_handler
from .print_utils import log_detailed, print_code, print_flush_status
from .config_utils import EndpointType


class SdkOperations:
    """
    Wrapper class for SDK operations with integrated detailed logging.
    
    This class wraps all SDK operations and adds detailed logging when
    USE_DETAILED_LOG environment variable is enabled. This keeps example
    code clean while providing comprehensive debugging information.
    
    Attributes:
        endpoint: The telemetry endpoint URL
        service_name: Service name for logging context
        service_version: Service version for logging context
        show_code: Whether to print code examples (default: True)
    """
    
    def __init__(self, endpoint: str = "", service_name: str = "", service_version: str = "", show_code: bool = True):
        """
        Initialize SDK operations wrapper.
        
        Args:
            endpoint: Target endpoint URL (optional, for logging)
            service_name: Service name (optional, for logging)
            service_version: Service version (optional, for logging)
            show_code: Whether to print code examples (default: True)
        """
        self.endpoint = endpoint
        self.service_name = service_name
        self.service_version = service_version
        self.show_code = show_code
    
    def _format_attributes(self, attributes: Optional[Dict[str, Any]]) -> str:
        """Format attributes for display in code examples."""
        if not attributes:
            return ""
        # Format as a compact dict representation
        items = [f'"{k}": {repr(v)}' for k, v in attributes.items()]
        return "{" + ", ".join(items) + "}"
    
    def create_configuration(
        self,
        endpoint: str,
        use_console: bool = False,
        metrics_interval_ms: Optional[int] = None,
        tracing_interval_ms: Optional[int] = None,
        logging_level: Optional[str] = None,
        skip_internet_check: bool = False,
        use_cumulative_metrics: bool = False,
        session_entropy: Optional[int] = None
    ) -> Configuration:
        """
        Create a Configuration object with detailed logging.
        
        Args:
            endpoint: Default endpoint URL
            use_console: Enable console exporter
            metrics_interval_ms: Metrics export interval in milliseconds
            tracing_interval_ms: Tracing export interval in milliseconds
            logging_level: Logging level (e.g., "info", "warning")
            skip_internet_check: Skip internet connectivity check
            use_cumulative_metrics: Use cumulative metrics aggregation
            session_entropy: Session entropy value
            
        Returns:
            Configured Configuration object
        """
        if self.show_code:
            print_code(f'config = Configuration(default_endpoint="{endpoint}")')
        
        log_detailed("Creating Configuration...")
        log_detailed(f"  -> Default endpoint: {endpoint}")
        
        config = Configuration(default_endpoint=endpoint)
        
        if use_console:
            if self.show_code:
                print_code('config.set_console_exporter(use_console=True)')
            config.set_console_exporter(use_console=True)
            log_detailed("  -> Console exporter enabled")
        
        if metrics_interval_ms:
            if self.show_code:
                print_code(f'config.set_metrics_export_interval_ms({metrics_interval_ms})')
            config.set_metrics_export_interval_ms(metrics_interval_ms)
            log_detailed(f"  -> Metrics export interval: {metrics_interval_ms}ms")
        
        if tracing_interval_ms:
            if self.show_code:
                print_code(f'config.set_tracing_export_interval_ms({tracing_interval_ms})')
            config.set_tracing_export_interval_ms(tracing_interval_ms)
            log_detailed(f"  -> Tracing export interval: {tracing_interval_ms}ms")
        
        if logging_level:
            if self.show_code:
                print_code(f'config.set_logging_level("{logging_level}")')
            config.set_logging_level(logging_level)
            log_detailed(f"  -> Logging level: {logging_level}")
        
        if skip_internet_check:
            if self.show_code:
                print_code('config.set_skip_internet_check(True)')
            config.set_skip_internet_check(True)
            log_detailed("  -> Internet check disabled")
        
        if use_cumulative_metrics:
            if self.show_code:
                print_code('config.set_use_cumulative_metrics(True)')
            config.set_use_cumulative_metrics(True)
            log_detailed("  -> Cumulative metrics enabled")
        
        if session_entropy:
            if self.show_code:
                print_code(f'config.set_tracing_session_entropy({session_entropy})')
            config.set_tracing_session_entropy(session_entropy)
            log_detailed(f"  -> Session entropy: {session_entropy}")
        
        log_detailed("[OK] Configuration created successfully")
        return config
    
    def create_attributes(
        self,
        service_name: str,
        service_version: str,
        platform: Optional[str] = None,
        environment: Optional[str] = None,
        hostname: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> ResourceAttributes:
        """
        Create ResourceAttributes object with detailed logging.
        
        Args:
            service_name: Service name (required)
            service_version: Service version (required)
            platform: Platform (e.g., "conda", "kubernetes")
            environment: Environment (e.g., "development", "production")
            hostname: Hostname
            user_id: User ID
            
        Returns:
            ResourceAttributes object
        """
        # Build code string
        if self.show_code:
            params = [f'service_name="{service_name}"', f'service_version="{service_version}"']
            if platform:
                params.append(f'platform="{platform}"')
            if environment:
                params.append(f'environment="{environment}"')
            if hostname:
                params.append(f'hostname="{hostname}"')
            if user_id:
                params.append(f'user_id="{user_id}"')
            print_code(f'attrs = ResourceAttributes({", ".join(params)})')
        
        log_detailed("Creating ResourceAttributes...")
        log_detailed(f"  -> Service name: {service_name}")
        log_detailed(f"  -> Service version: {service_version}")
        
        kwargs = {}
        if platform:
            kwargs['platform'] = platform
            log_detailed(f"  -> Platform: {platform}")
        if environment:
            kwargs['environment'] = environment
            log_detailed(f"  -> Environment: {environment}")
        if hostname:
            kwargs['hostname'] = hostname
            log_detailed(f"  -> Hostname: {hostname}")
        if user_id:
            kwargs['user_id'] = user_id
            log_detailed(f"  -> User ID: {user_id}")
        
        attrs = ResourceAttributes(
            service_name=service_name,
            service_version=service_version,
            **kwargs
        )
        
        log_detailed("[OK] ResourceAttributes created successfully")
        return attrs
    
    def set_custom_attributes(
        self,
        attrs: ResourceAttributes,
        **custom_attrs
    ) -> None:
        """
        Set custom attributes on ResourceAttributes with detailed logging.
        
        Args:
            attrs: ResourceAttributes object to update
            **custom_attrs: Custom attributes as keyword arguments
        """
        if not custom_attrs:
            return
        
        if self.show_code:
            attrs_str = ", ".join(f'{k}="{v}"' for k, v in custom_attrs.items())
            print_code(f'attrs.set_attributes({attrs_str})')
        
        log_detailed("Setting custom attributes...")
        for key, value in custom_attrs.items():
            log_detailed(f"  -> {key}: {value}")
        
        attrs.set_attributes(**custom_attrs)
        log_detailed("[OK] Custom attributes set successfully")
    
    def initialize(
        self,
        config: Configuration,
        attributes: ResourceAttributes,
        signal_types: Optional[List[str]] = None
    ) -> None:
        """
        Initialize telemetry with detailed logging.
        
        Args:
            config: Configuration object
            attributes: Resource attributes
            signal_types: List of signal types to enable
        """
        # Print the code being executed
        if self.show_code:
            signal_str = f"signal_types={signal_types}" if signal_types else ""
            print_code(f"initialize_telemetry(config, attrs{', ' + signal_str if signal_str else ''})")
        
        log_detailed("Calling initialize_telemetry()...")
        log_detailed(f"  Config: endpoint={self.endpoint}")
        log_detailed(f"  Attributes: service_name={self.service_name}, service_version={self.service_version}")
        log_detailed(f"  Signal types: {signal_types}")
        
        start_time = time.time()
        # Only pass signal_types if it's not None to use the default value
        if signal_types is not None:
            log_detailed(f"  -> Passing signal_types explicitly: {signal_types}")
            initialize_telemetry(
                config=config,
                attributes=attributes,
                signal_types=signal_types
            )
        else:
            log_detailed("  -> Using default signal_types (not passing parameter)")
            initialize_telemetry(
                config=config,
                attributes=attributes
            )
        duration = time.time() - start_time
        
        log_detailed(f"[OK] Initialization completed in {duration:.3f}s")
        
        # Log which providers are ready
        if signal_types:
            for signal in signal_types:
                log_detailed(f"[OK] {signal.capitalize()} provider ready to accept {signal}")
    
    def get_logger(self, logger_name: str, level: int = logging.INFO) -> logging.Logger:
        """
        Get a logger configured with telemetry handler.
        
        Args:
            logger_name: Name of the logger
            level: Logging level (default: logging.INFO)
            
        Returns:
            Configured logger instance
        """
        if self.show_code:
            level_name = logging.getLevelName(level)
            print_code(f'logger = logging.getLogger("{logger_name}")')
            if level != logging.INFO:
                print_code(f'logger.setLevel(logging.{level_name})')
        
        log_detailed(f"Creating logger: {logger_name}")
        log_detailed(f"  -> Level: {logging.getLevelName(level)}")
        
        # Get the telemetry handler
        handler = get_telemetry_logger_handler()
        
        # Create and configure logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.addHandler(handler)
        
        log_detailed(f"[OK] Logger '{logger_name}' configured with telemetry handler")
        
        return logger
    
    def increment_counter(
        self,
        name: str,
        by: Union[int, float] = 1,
        attributes: Optional[Dict[str, Any]] = None,
        description: str = ""
    ) -> None:
        """
        Increment a counter with detailed logging.
        
        Args:
            name: Counter name
            by: Amount to increment by
            attributes: Optional attributes dictionary
            description: Optional description for logging
        """
        # Print the code being executed
        if self.show_code:
            attrs_str = f", attributes={self._format_attributes(attributes)}" if attributes else ""
            by_str = f", by={by}" if by != 1 else ""
            print_code(f'increment_counter("{name}"{by_str}{attrs_str})')
        
        # Build log message
        log_msg = f"Sending counter: {name}"
        if description:
            log_msg += f" ({description})"
        log_detailed(log_msg)
        
        log_detailed(f"  -> Metric: {name}")
        log_detailed(f"  -> Value: {by}")
        if attributes:
            log_detailed(f"  -> Attributes: {attributes}")
        if self.endpoint:
            log_detailed(f"  -> Endpoint: {self.endpoint}")
        
        start_time = time.time()
        increment_counter(name, by=by, attributes=attributes or {})
        duration = time.time() - start_time
        
        log_detailed(f"[OK] Counter queued successfully (took {duration:.3f}s)")
        log_detailed("[OK] SDK accepted metric, will export in background")
    
    def record_histogram(
        self,
        name: str,
        value: Union[int, float],
        attributes: Optional[Dict[str, Any]] = None,
        description: str = ""
    ) -> None:
        """
        Record a histogram value with detailed logging.
        
        Args:
            name: Histogram name
            value: Value to record
            attributes: Optional attributes dictionary
            description: Optional description for logging
        """
        # Print the code being executed
        if self.show_code:
            attrs_str = f", attributes={self._format_attributes(attributes)}" if attributes else ""
            print_code(f'record_histogram("{name}", {value}{attrs_str})')
        
        # Build log message
        log_msg = f"Sending histogram: {name}"
        if description:
            log_msg += f" ({description})"
        log_detailed(log_msg)
        
        log_detailed(f"  -> Metric: {name}")
        log_detailed(f"  -> Value: {value}")
        if attributes:
            log_detailed(f"  -> Attributes: {attributes}")
        if self.endpoint:
            log_detailed(f"  -> Endpoint: {self.endpoint}")
        
        start_time = time.time()
        record_histogram(name, value, attributes=attributes or {})
        duration = time.time() - start_time
        
        log_detailed(f"[OK] Histogram queued successfully (took {duration:.3f}s)")
        log_detailed("[OK] SDK accepted metric, will export in background")
    
    def record_histogram_batch(
        self,
        name: str,
        values: List[Union[int, float]],
        attributes: Optional[Dict[str, Any]] = None,
        description: str = ""
    ) -> None:
        """
        Record multiple histogram values with detailed logging.
        
        This is useful when recording multiple measurements for the same
        metric with the same attributes (e.g., multiple latency samples).
        
        Args:
            name: Histogram name
            values: List of values to record
            attributes: Optional attributes dictionary
            description: Optional description for logging
        """
        # Print the code being executed (show loop pattern)
        if self.show_code:
            attrs_str = f", attributes={self._format_attributes(attributes)}" if attributes else ""
            print_code(f'record_histogram("{name}", value{attrs_str})  # {len(values)} times')
        
        # Build log message
        log_msg = f"Sending histograms: {name}"
        if description:
            log_msg += f" ({description})"
        log_detailed(log_msg)
        
        log_detailed(f"  -> Metric: {name}")
        if attributes:
            log_detailed(f"  -> Attributes: {attributes}")
        log_detailed(f"  -> Values: {values}")
        
        start_time = time.time()
        for i, value in enumerate(values, 1):
            record_histogram(name, value, attributes=attributes or {})
            log_detailed(f"  -> Histogram {i}/{len(values)}: {value} queued")
        total_duration = time.time() - start_time
        
        log_detailed(f"[OK] All {len(values)} histograms queued successfully (took {total_duration:.3f}s)")
        log_detailed("[OK] SDK accepted metrics, will export in background")
    
    def decrement_counter(
        self,
        name: str,
        by: Union[int, float] = 1,
        attributes: Optional[Dict[str, Any]] = None,
        description: str = ""
    ) -> None:
        """
        Decrement a counter with detailed logging.
        
        Args:
            name: Counter name
            by: Amount to decrement by
            attributes: Optional attributes dictionary
            description: Optional description for logging
        """
        # Print the code being executed
        if self.show_code:
            attrs_str = f", attributes={self._format_attributes(attributes)}" if attributes else ""
            by_str = f", by={by}" if by != 1 else ""
            print_code(f'decrement_counter("{name}"{by_str}{attrs_str})')
        
        # Build log message
        log_msg = f"Sending decrement counter: {name}"
        if description:
            log_msg += f" ({description})"
        log_detailed(log_msg)
        
        log_detailed(f"  -> Metric: {name}")
        log_detailed(f"  -> Value: -{by}")
        if attributes:
            log_detailed(f"  -> Attributes: {attributes}")
        if self.endpoint:
            log_detailed(f"  -> Endpoint: {self.endpoint}")
        
        start_time = time.time()
        decrement_counter(name, by=by, attributes=attributes or {})
        duration = time.time() - start_time
        
        log_detailed(f"[OK] Counter decremented successfully (took {duration:.3f}s)")
        log_detailed("[OK] SDK accepted metric, will export in background")
    
    def apply_signal_specific_endpoints(self, config: Configuration, endpoints: dict) -> None:
        """
        Apply signal-specific endpoints to a Configuration object if they are provided.
        
        This is a utility function to reduce code duplication when setting up
        signal-specific endpoints (logging, metrics, tracing).
        
        Args:
            config: Configuration object to update
            endpoints: Dictionary with endpoint values (from load_environment())
        
        Example:
            >>> sdk = SdkOperations()
            >>> _, endpoint, _, endpoints = load_environment()
            >>> config = Configuration(default_endpoint=endpoint)
            >>> sdk.apply_signal_specific_endpoints(config, endpoints)
        """
        if endpoints.get(EndpointType.LOGGING.value):
            config.set_logging_endpoint(endpoints[EndpointType.LOGGING.value])
        if endpoints.get(EndpointType.METRICS.value):
            config.set_metrics_endpoint(endpoints[EndpointType.METRICS.value])
        if endpoints.get(EndpointType.TRACING.value):
            config.set_tracing_endpoint(endpoints[EndpointType.TRACING.value])
    
    def set_signal_endpoints(
        self,
        config: Configuration,
        metrics_endpoint: Optional[str] = None,
        logging_endpoint: Optional[str] = None,
        tracing_endpoint: Optional[str] = None
    ) -> None:
        """
        Set individual signal-specific endpoints with detailed logging.
        
        Args:
            config: Configuration object to update
            metrics_endpoint: Optional metrics endpoint URL
            logging_endpoint: Optional logging endpoint URL
            tracing_endpoint: Optional tracing endpoint URL
        
        Example:
            >>> sdk = SdkOperations()
            >>> config = sdk.create_configuration(endpoint="http://localhost:4318")
            >>> sdk.set_signal_endpoints(
            ...     config,
            ...     metrics_endpoint="http://metrics:4318",
            ...     logging_endpoint="http://logs:4318",
            ...     tracing_endpoint="http://traces:4318"
            ... )
        """
        if self.show_code:
            if metrics_endpoint:
                print_code(f'config.set_metrics_endpoint("{metrics_endpoint}")')
            if logging_endpoint:
                print_code(f'config.set_logging_endpoint("{logging_endpoint}")')
            if tracing_endpoint:
                print_code(f'config.set_tracing_endpoint("{tracing_endpoint}")')
        
        if metrics_endpoint:
            log_detailed(f"Setting metrics endpoint: {metrics_endpoint}")
            config.set_metrics_endpoint(metrics_endpoint)
            log_detailed("[OK] Metrics endpoint set")
        
        if logging_endpoint:
            log_detailed(f"Setting logging endpoint: {logging_endpoint}")
            config.set_logging_endpoint(logging_endpoint)
            log_detailed("[OK] Logging endpoint set")
        
        if tracing_endpoint:
            log_detailed(f"Setting tracing endpoint: {tracing_endpoint}")
            config.set_tracing_endpoint(tracing_endpoint)
            log_detailed("[OK] Tracing endpoint set")
    
    def flush_metrics(self, timeout_millis: int = 5000) -> None:
        """
        Flush metrics provider with detailed logging.
        
        Args:
            timeout_millis: Timeout in milliseconds (default: 5000)
        """
        if self.show_code:
            print_code(f'# Flush metrics (timeout: {timeout_millis}ms)')
        
        log_detailed("Flushing metrics provider...")
        log_detailed(f"  -> Timeout: {timeout_millis}ms")
        
        start_time = time.time()
        meter_provider = metrics.get_meter_provider()
        if hasattr(meter_provider, 'force_flush'):
            meter_provider.force_flush(timeout_millis=timeout_millis)
        duration = time.time() - start_time
        
        log_detailed(f"[OK] Metrics flushed successfully (took {duration:.3f}s)")
    
    def flush_traces(self, timeout_millis: int = 5000) -> None:
        """
        Flush traces provider with detailed logging.
        
        Args:
            timeout_millis: Timeout in milliseconds (default: 5000)
        """
        if self.show_code:
            print_code(f'# Flush traces (timeout: {timeout_millis}ms)')
        
        log_detailed("Flushing traces provider...")
        log_detailed(f"  -> Timeout: {timeout_millis}ms")
        
        start_time = time.time()
        tracer_provider = trace.get_tracer_provider()
        if hasattr(tracer_provider, 'force_flush'):
            tracer_provider.force_flush(timeout_millis=timeout_millis)
        duration = time.time() - start_time
        
        log_detailed(f"[OK] Traces flushed successfully (took {duration:.3f}s)")
    
    def flush_logs(self, timeout_millis: int = 5000) -> None:
        """
        Flush logs provider with detailed logging.
        
        Args:
            timeout_millis: Timeout in milliseconds (default: 5000)
        """
        if self.show_code:
            print_code(f'# Flush logs (timeout: {timeout_millis}ms)')
        
        log_detailed("Flushing logs provider...")
        log_detailed(f"  -> Timeout: {timeout_millis}ms")
        
        start_time = time.time()
        if _AnacondaLogger._instance:
            logger_instance = _AnacondaLogger._instance
            if hasattr(logger_instance, '_provider') and logger_instance._provider:
                logger_instance._provider.force_flush(timeout_millis=timeout_millis)
        duration = time.time() - start_time
        
        log_detailed(f"[OK] Logs flushed successfully (took {duration:.3f}s)")
    
    def flush_telemetry(self) -> None:
        """
        Flush all telemetry providers (metrics, traces, logs) with detailed logging.
        
        This is a convenience method that calls flush_metrics(), flush_traces(),
        and flush_logs() in sequence. Use the individual methods if you only
        need to flush specific providers.
        """
        if self.show_code:
            print_code('# Flush all telemetry data')
        
        log_detailed("Flushing all telemetry providers...")
        
        start_time = time.time()
        self.flush_metrics()
        self.flush_traces()
        self.flush_logs()
        total_duration = time.time() - start_time
        
        log_detailed(f"[OK] All telemetry flushed successfully (total: {total_duration:.3f}s)")
        print_flush_status(success=True)
    
    def get_trace(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """
        Create a trace span context manager with detailed logging.
        
        Args:
            name: Span name
            attributes: Optional attributes dictionary
            
        Returns:
            Context manager for the trace span
            
        Example:
            >>> with sdk.get_trace("api_request", attributes={"http.method": "GET"}):
            ...     # Your code here
            ...     pass
        """
        if self.show_code:
            attrs_str = f", attributes={self._format_attributes(attributes)}" if attributes else ""
            print_code(f'with get_trace("{name}"{attrs_str}) as span:')
        
        log_detailed(f"Creating trace span: {name}")
        if attributes:
            log_detailed(f"  -> Attributes: {attributes}")
        
        return get_trace(name, attributes=attributes or {})
