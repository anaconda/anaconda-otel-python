#!/usr/bin/env python3
"""
Example 4: Selective Signals

Demonstrates initializing telemetry with only specific signals (metrics + tracing).
This is a standalone script to ensure proper initialization.

WHEN TO USE THIS APPROACH:
- You need a specific combination of signals (not all, not just one)
- You want distributed tracing but don't need structured logging
- You need to balance observability needs with resource constraints
- You want to optimize for specific use cases

USE CASES:
- Microservices that need request tracing and metrics but use external logging
- Services where you want to trace request flows and measure performance
- Applications that already have logging infrastructure but need telemetry
- Scenarios where you need metrics and traces but logging is handled separately
- Performance optimization: enable only the signals you actively use

EXAMPLE COMBINATIONS:
- metrics + tracing: Track performance and trace request flows (this example)
- metrics + logging: Measure and log without distributed tracing
- logging + tracing: Detailed logs with trace context (no metrics)
"""

from anaconda.opentelemetry import Configuration, ResourceAttributes, initialize_telemetry, increment_counter
from utils import (
    EndpointType,
    load_environment,
    print_header,
    print_footer,
    print_info,
    print_code,
    print_environment_config,
    print_resource_attributes,
    print_metric_info,
    print_backend_validation,
    print_sdk_commands_summary,
    apply_signal_specific_endpoints
)
from test_data import ServiceName, ServiceVersion, MetricName, MetricValue, SignalTypes, CustomAttributes

# Test data constants
SERVICE_NAME = ServiceName.EXAMPLE_04.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
METRIC_NAME = MetricName.EXAMPLE_04.value
METRIC_VALUE = MetricValue.INCREMENT_BY_ONE.value


def main():
    print_header("Example 4: Selective Signals",
                 "Initialize with only specific signals (metrics + tracing)")
    
    # Load environment
    _, endpoint, use_console, endpoints = load_environment()
    print_environment_config(endpoint, use_console)
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    apply_signal_specific_endpoints(config, endpoints)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    # Create attributes
    attrs = ResourceAttributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    print_code(f'attrs = ResourceAttributes(service_name="{SERVICE_NAME}", service_version="{SERVICE_VERSION}")')
    
    # Add custom attributes for this example
    custom_attrs = CustomAttributes.EXAMPLE_04.value
    attrs.set_attributes(**custom_attrs)
    print_code(f'attrs.set_attributes({", ".join(f"{k}=\"{v}\"" for k, v in custom_attrs.items())})')
    print_info(f"✓ Custom attributes added: {custom_attrs}")
    
    # Initialize with selective signals
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=SignalTypes.METRICS_AND_TRACING.value
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics', 'tracing'])")
    
    print_info("✓ Telemetry initialized with selective signals")
    print_info("Enabled: metrics, traces")
    print_info("Disabled: logs")
    
    # Print SDK commands summary
    print_sdk_commands_summary([
        'config = Configuration(default_endpoint=...)',
        'attrs = ResourceAttributes(service_name="...", service_version="...")',
        'attrs.set_attributes(key1="value1", key2="value2")',
        "initialize_telemetry(config, attrs, signal_types=['metrics', 'tracing'])",
        'increment_counter("metric_name", by=1)',
    ])
    
    # Print resource attributes
    print_resource_attributes(attrs)
    
    # Send a test metric
    increment_counter(METRIC_NAME, by=METRIC_VALUE)
    print_metric_info(METRIC_NAME, METRIC_VALUE)
    
    # Print backend validation checklist
    print_backend_validation(SERVICE_NAME, METRIC_NAME, METRIC_VALUE, attrs)
    
    print_footer("✓ Example 4 completed successfully!")


if __name__ == "__main__":
    main()
