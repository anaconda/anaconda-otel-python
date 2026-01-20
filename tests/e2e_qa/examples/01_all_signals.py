#!/usr/bin/env python3
"""
Example 1: Initialize All Signals

Demonstrates initializing telemetry with metrics, logs, and traces.
This is a standalone script to ensure proper initialization.

WHEN TO USE THIS APPROACH:
- You need comprehensive observability across all signal types
- Your application requires metrics, structured logging, and distributed tracing
- You want full visibility into application behavior and performance
- You're building a production service that needs complete telemetry coverage

USE CASES:
- Microservices that need end-to-end tracing
- Applications with complex workflows requiring detailed logging
- Services where you need to correlate metrics, logs, and traces
- Production environments requiring full observability
"""

from anaconda.opentelemetry import Configuration, ResourceAttributes, initialize_telemetry, increment_counter
from utils import (
    load_environment,
    print_header,
    print_footer,
    print_info,
    print_code,
    print_environment_config,
    print_resource_attributes,
    print_metric_info,
    print_backend_validation,
    print_sdk_commands_summary
)
from test_data import (
    ServiceName,
    ServiceVersion,
    MetricName,
    MetricValue,
    SignalTypes,
    AutoDetectedAttributes,
    CustomAttributes
)

# Test data constants
SERVICE_NAME = ServiceName.EXAMPLE_01.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
METRIC_NAME = MetricName.EXAMPLE_01.value
METRIC_VALUE = MetricValue.INCREMENT_BY_ONE.value
AUTO_DETECTED_ATTRS = AutoDetectedAttributes.STANDARD.value


def main():
    print_header("Example 1: Initialize All Signals", 
                 "Initialize telemetry with metrics, logs, and traces")
    
    # Load environment
    _, endpoint, use_console = load_environment()
    print_environment_config(endpoint, use_console)
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    # Create attributes
    attrs = ResourceAttributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    print_code(f'attrs = ResourceAttributes(service_name="{SERVICE_NAME}", service_version="{SERVICE_VERSION}")')
    
    # Add custom attributes for this example
    custom_attrs = CustomAttributes.EXAMPLE_01.value
    attrs.set_attributes(**custom_attrs)
    print_code(f'attrs.set_attributes({", ".join(f"{k}=\"{v}\"" for k, v in custom_attrs.items())})')
    print_info(f"✓ Custom attributes added: {custom_attrs}")
    
    # Initialize with all signals
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=SignalTypes.ALL_SIGNALS.value
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics', 'logging', 'tracing'])")
    
    print_info("✓ Telemetry initialized with all signals")
    print_info("Enabled: metrics, logs, traces")
    
    # Print SDK commands summary
    print_sdk_commands_summary([
        'config = Configuration(default_endpoint=...)',
        'attrs = ResourceAttributes(service_name="...", service_version="...")',
        'attrs.set_attributes(key1="value1", key2="value2")',
        "initialize_telemetry(config, attrs, signal_types=['metrics', 'logging', 'tracing'])",
        'increment_counter("metric_name", by=1)',
    ])
    
    # Print resource attributes
    print_resource_attributes(attrs)
    
    # Send a test metric
    increment_counter(METRIC_NAME, by=METRIC_VALUE)
    print_metric_info(METRIC_NAME, METRIC_VALUE)
    
    # Print backend validation checklist
    print_backend_validation(SERVICE_NAME, METRIC_NAME, METRIC_VALUE, attrs)
    
    print_footer("✓ Example 1 completed successfully!")


if __name__ == "__main__":
    main()
