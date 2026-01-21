#!/usr/bin/env python3
"""
Example 7: Explicit Flush Test

Demonstrates explicit flush functionality to ensure it doesn't break the telemetry flow.
This is a standalone script to ensure proper initialization with flush.

WHEN TO USE THIS APPROACH:
- You need to ensure telemetry data is sent before the application exits
- You're running short-lived processes or scripts
- You want to force immediate export of pending telemetry data
- You need to verify telemetry was sent before proceeding

USE CASES:
- Short-lived CLI tools or batch jobs
- Lambda functions or serverless applications
- Testing and validation scenarios
- Applications where you need guaranteed delivery before shutdown
- Scripts that need to confirm telemetry export completed

NOTE: For Python, the OpenTelemetry SDK automatically handles flushing when
the process ends. Explicit flush is typically not necessary but is supported
for cases where you need immediate export or want to ensure data is sent
before continuing execution.
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
SERVICE_NAME = ServiceName.EXAMPLE_07.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
METRIC_NAME = MetricName.EXAMPLE_07.value
METRIC_VALUE = MetricValue.INCREMENT_BY_ONE.value
AUTO_DETECTED_ATTRS = AutoDetectedAttributes.STANDARD.value


def main():
    print_header("Example 7: Explicit Flush Test", 
                 "Verify flush functionality doesn't break telemetry flow")
    
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
    custom_attrs = CustomAttributes.EXAMPLE_07.value
    sdk.set_custom_attributes(attrs, **custom_attrs)
    
    # Initialize with all signals
    sdk.initialize(config, attrs, signal_types=SignalTypes.ALL_SIGNALS.value)
    
    # Send a test metric
    sdk.increment_counter(METRIC_NAME, by=METRIC_VALUE)
    
    # Explicitly flush telemetry
    sdk.flush_telemetry()
    
    print_footer("✓ Example 7 completed successfully!")


if __name__ == "__main__":
    main()
