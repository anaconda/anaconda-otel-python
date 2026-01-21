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

from utils import (
    load_environment,
    print_header,
    print_footer,
    print_info,
    print_environment_config,
    SdkOperations
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
    
    # Initialize SDK operations wrapper
    sdk = SdkOperations(
        endpoint=endpoint,
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Create configuration
    config = sdk.create_configuration(endpoint=endpoint, use_console=use_console)
    sdk.apply_signal_specific_endpoints(config, endpoints)
    
    # Create attributes
    attrs = sdk.create_attributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Add custom attributes for this example
    custom_attrs = CustomAttributes.EXAMPLE_04.value
    sdk.set_custom_attributes(attrs, **custom_attrs)
    
    # Initialize with selective signals
    sdk.initialize(config, attrs, signal_types=SignalTypes.METRICS_AND_TRACING.value)
    print_info("Disabled: logs")
    
    # Send a test metric
    sdk.increment_counter(METRIC_NAME, by=METRIC_VALUE)
    
    print_footer("✓ Example 4 completed successfully!")


if __name__ == "__main__":
    main()
