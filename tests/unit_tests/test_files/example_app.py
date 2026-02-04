# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

import sys
sys.path.append("./")

import random, logging
from io import StringIO

from anaconda_opentelemetry.attributes import ResourceAttributes
from anaconda_opentelemetry.config import Configuration
from anaconda_opentelemetry.signals import (
    initialize_telemetry,
    get_telemetry_logger_handler,
    record_histogram,
    increment_counter,
    get_trace,
    _AnacondaLogger
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExampleApp:
    """Example application that generates various telemetry signals."""

    def __init__(
            self,
            service_name: str = "test-service",
            service_version: str = "0.1.0",
            otel_endpoint: str = "http://localhost:4317",
            use_console_exporter: bool = True
    ):
        """
        Initialize the example app with telemetry.

        Args:
            service_name: Name of the service creating telemetry
            service_version: Version of service creating telemetry
            otel_endpoint: Optional OTLP endpoint (defaults to localhost:4317)
            use_console_exporter: Whether to use console exporter or not
        """
        self.service_name = service_name
        # initialize required classes
        attrs = ResourceAttributes(service_name, service_version)
        config = Configuration(default_endpoint=otel_endpoint)

        config.set_console_exporter(use_console=use_console_exporter)
        attrs.set_attributes(**{"cheese": "american", "test": "hello"})

        # initialize package
        initialize_telemetry(config, attrs, signal_types=["logging", "tracing", "metrics"])

        # inject logger
        logger.addHandler(get_telemetry_logger_handler())

    def remove_handler(self):
        logger.removeHandler(get_telemetry_logger_handler())

    def export_log(self) -> None:
        """Simulate a user request with various telemetry signals."""

        # send log
        logger.warning(f"Test warning. Initialized telemetry for integration test.")

    def export_trace(self) -> None:
        # send trace
        with get_trace("user_request") as span:
            # Add span attributes
            span.add_event("test", attributes={"request.type": "api_call"})

    def export_metric(self) -> None:

        # Increment request counter
        increment_counter(
            "http_requests_total",
            by=1,
            attributes={"method": "GET", "endpoint": "/api/data"}
        )

        # Simulate processing time
        processing_time = random.uniform(0.1, 0.5)
        # Record processing time histogram
        record_histogram(
            "request_duration_seconds",
            value=processing_time,
            attributes={"endpoint": "/api/data"}
        )


def simulate_metric() -> str:
    from opentelemetry import metrics

    # Create ExampleApp first
    example = ExampleApp()

    # Access the exporter through the meter provider
    mock_out = StringIO()
    meter_provider = metrics.get_meter_provider()

    # Find the ConsoleMetricExporter in the metric readers
    exporter_found = False
    if hasattr(meter_provider, '_all_metric_readers'):
        # Iterate through _all_metric_readers
        for reader_ref in meter_provider._all_metric_readers:
            if hasattr(reader_ref, '_exporter'):
                exporter = reader_ref._exporter
                # Check if it's a ConsoleMetricExporter
                if exporter.__class__.__name__ == 'ConsoleMetricExporter':
                    # Replace its out attribute
                    exporter.out = mock_out
                    exporter_found = True
                    break

    if not exporter_found:
        raise RuntimeError("ConsoleMetricExporter not found in metric readers")

    # Run the simulation
    example.export_metric()

    # Force metrics to export
    meter_provider.force_flush(timeout_millis=10000)

    return mock_out.getvalue()

def simulate_log() -> str:
    # Create ExampleApp with logging enabled
    example = ExampleApp(use_console_exporter=True)

    # Create a StringIO object to capture output
    mock_out = StringIO()

    # Find the LoggingHandler
    inst: _AnacondaLogger = _AnacondaLogger._instance
    saved = inst._test_set_console_mock(mock_out)

    example.export_log()

    # Force flush logs to ensure they're written to our StringIO
    inst._provider.force_flush()

    # Restore logger state
    inst._test_set_console_mock(saved)
    example.remove_handler()

    # return outout as a string
    return mock_out.getvalue()

def simulate_trace() -> str:
    from opentelemetry import trace
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    # Create ExampleApp with logging enabled
    example = ExampleApp(use_console_exporter=True)

    # Create a StringIO object to capture output
    mock_out = StringIO()
    exporter_found = False

    # get trace provider
    trace_provider = trace.get_tracer_provider()

    if hasattr(trace_provider, '_active_span_processor'):
        provider_span_processors = trace_provider._active_span_processor
        if hasattr(provider_span_processors, '_span_processors'):
            processors = provider_span_processors._span_processors
            for processor in processors:
                if isinstance(processor, BatchSpanProcessor):
                    # Access the exporter through the processor
                    if hasattr(processor, 'span_exporter'):
                        exporter = processor.span_exporter
                        if isinstance(exporter, ConsoleSpanExporter):
                            # Replace its out attribute
                            exporter.out = mock_out
                            exporter_found = True
                            break

                if exporter_found:
                    break

    if not exporter_found:
        raise RuntimeError("ConsoleSpanExporter not found in tracer providers")

    # Send a log to stdout
    example.export_trace()

    # force flush
    trace_provider.force_flush()

    return mock_out.getvalue()