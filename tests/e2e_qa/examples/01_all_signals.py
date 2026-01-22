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

from utils import (
    load_environment,
    print_header,
    print_footer,
    print_info,
    print_environment_config,
    SdkOperations,
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
    custom_attrs = CustomAttributes.EXAMPLE_01.value
    sdk.set_custom_attributes(attrs, **custom_attrs)
    
    # Initialize with all signals
    sdk.initialize(config, attrs, signal_types=SignalTypes.ALL_SIGNALS.value)
    
    # Send a test metric
    sdk.increment_counter(METRIC_NAME, by=METRIC_VALUE)
    
    print_footer("[OK] Example 1 completed successfully!")


if __name__ == "__main__":
    main()
