#!/usr/bin/env python3
"""
Example 3: Default Initialization

Demonstrates initializing telemetry with default settings (metrics only).
This is a standalone script to ensure proper initialization.

WHEN TO USE THIS APPROACH:
- You want the simplest possible initialization with minimal configuration
- You're getting started and want to use SDK defaults
- You don't need to explicitly specify signal types (defaults to metrics)
- You want the most concise code with standard behavior

USE CASES:
- Quick prototyping or proof-of-concept implementations
- Simple applications where default behavior is sufficient
- Learning the SDK basics without complexity
- When you want metrics but prefer implicit over explicit configuration
- Scripts or utilities where brevity is preferred

NOTE: This is functionally equivalent to Example 2 (metrics only) but uses
implicit defaults rather than explicit signal_types parameter.
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
from test_data import ServiceName, ServiceVersion, MetricName, MetricValue, CustomAttributes

# Test data constants
SERVICE_NAME = ServiceName.EXAMPLE_03.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
METRIC_NAME = MetricName.EXAMPLE_03.value
METRIC_VALUE = MetricValue.INCREMENT_BY_ONE.value


def main():
    print_header("Example 3: Default Initialization",
                 "Initialize with default settings (no signals parameter)")
    
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
    custom_attrs = CustomAttributes.EXAMPLE_03.value
    attrs.set_attributes(**custom_attrs)
    print_code(f'attrs.set_attributes({", ".join(f"{k}=\"{v}\"" for k, v in custom_attrs.items())})')
    print_info(f"✓ Custom attributes added: {custom_attrs}")
    
    # Initialize with default (metrics only)
    initialize_telemetry(
        config=config,
        attributes=attrs
    )
    print_code("initialize_telemetry(config, attrs)  # No signal_types = defaults to metrics")
    
    print_info("✓ Telemetry initialized with defaults")
    print_info("Default behavior: metrics signal enabled")
    
    # Print SDK commands summary
    print_sdk_commands_summary([
        'config = Configuration(default_endpoint=...)',
        'attrs = ResourceAttributes(service_name="...", service_version="...")',
        'attrs.set_attributes(key1="value1", key2="value2")',
        'initialize_telemetry(config, attrs)  # No signal_types = defaults to metrics',
        'increment_counter("metric_name", by=1)',
    ])
    
    # Print resource attributes
    print_resource_attributes(attrs)
    
    # Send a test metric
    increment_counter(METRIC_NAME, by=METRIC_VALUE)
    print_metric_info(METRIC_NAME, METRIC_VALUE)
    
    # Print backend validation checklist
    print_backend_validation(SERVICE_NAME, METRIC_NAME, METRIC_VALUE, attrs)
    
    print_footer("✓ Example 3 completed successfully!")


if __name__ == "__main__":
    main()
