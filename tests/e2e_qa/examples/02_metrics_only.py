#!/usr/bin/env python3
"""
Example 2: Initialize Metrics Only

Demonstrates initializing telemetry with only the metrics signal.
This is a standalone script to ensure proper initialization.

WHEN TO USE THIS APPROACH:
- You only need to track counters, gauges, and histograms
- You want minimal overhead and resource usage
- Your application doesn't require logging or tracing capabilities
- You're monitoring simple metrics like request counts, response times, or resource usage

USE CASES:
- Batch jobs that only need to report completion metrics
- Background workers tracking task counts and durations
- Simple services where metrics alone provide sufficient visibility
- Performance-sensitive applications minimizing telemetry overhead
- CLI tools or scripts that only need basic instrumentation
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
SERVICE_NAME = ServiceName.EXAMPLE_02.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
METRIC_NAME = MetricName.EXAMPLE_02.value
METRIC_VALUE = MetricValue.INCREMENT_BY_ONE.value
AUTO_DETECTED_ATTRS = AutoDetectedAttributes.STANDARD.value


def main():
    print_header("Example 2: Initialize Metrics Only",
                 "Initialize telemetry with only metrics signal")
    
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
    custom_attrs = CustomAttributes.EXAMPLE_02.value
    attrs.set_attributes(**custom_attrs)
    print_code(f'attrs.set_attributes({", ".join(f"{k}=\"{v}\"" for k, v in custom_attrs.items())})')
    print_info(f"✓ Custom attributes added: {custom_attrs}")
    
    # Initialize with metrics only
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=SignalTypes.METRICS_ONLY.value
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics'])")
    
    print_info("✓ Telemetry initialized with metrics only")
    print_info("Enabled: metrics")
    
    # Print SDK commands summary
    print_sdk_commands_summary([
        'config = Configuration(default_endpoint=...)',
        'attrs = ResourceAttributes(service_name="...", service_version="...")',
        'attrs.set_attributes(key1="value1", key2="value2")',
        "initialize_telemetry(config, attrs, signal_types=['metrics'])",
        'increment_counter("metric_name", by=1)',
    ])
    
    # Print resource attributes
    print_resource_attributes(attrs)
    
    # Send a test metric
    increment_counter(METRIC_NAME, by=METRIC_VALUE)
    print_metric_info(METRIC_NAME, METRIC_VALUE)
    
    # Print backend validation checklist
    print_backend_validation(SERVICE_NAME, METRIC_NAME, METRIC_VALUE, attrs)
    
    print_footer("✓ Example 2 completed successfully!")


if __name__ == "__main__":
    main()
