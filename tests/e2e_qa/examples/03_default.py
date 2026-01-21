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

from utils import (
    load_environment,
    print_header,
    print_footer,
    print_info,
    print_environment_config,
    SdkOperations
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
    custom_attrs = CustomAttributes.EXAMPLE_03.value
    sdk.set_custom_attributes(attrs, **custom_attrs)
    
    # Initialize with default (metrics only)
    sdk.initialize(config, attrs)
    
    # Send a test metric
    sdk.increment_counter(METRIC_NAME, by=METRIC_VALUE)
    
    print_footer("✓ Example 3 completed successfully!")


if __name__ == "__main__":
    main()
