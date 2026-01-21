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

from utils import (
    load_environment,
    print_header,
    print_footer,
    print_info,
    print_environment_config,
    SdkOperations
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
    custom_attrs = CustomAttributes.EXAMPLE_02.value
    sdk.set_custom_attributes(attrs, **custom_attrs)
    
    # Initialize with metrics only
    sdk.initialize(config, attrs, signal_types=SignalTypes.METRICS_ONLY.value)
    
    # Send a test metric
    sdk.increment_counter(METRIC_NAME, by=METRIC_VALUE)
    
    print_footer("✓ Example 2 completed successfully!")


if __name__ == "__main__":
    main()
