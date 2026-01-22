#!/usr/bin/env python3
"""
Example 5: Complete Initialization

Demonstrates comprehensive initialization with all configuration options.
This is a standalone script to ensure proper initialization.

WHEN TO USE THIS APPROACH:
- You need fine-grained control over all configuration options
- You're setting up production-ready telemetry with specific requirements
- You need to configure export intervals, logging levels, and custom attributes
- You want to see all available configuration options in one place

USE CASES:
- Production services requiring specific export intervals and logging levels
- Applications with custom attributes for environment, platform, or team metadata
- Services that need to tune telemetry behavior for performance or compliance
- Reference implementation showing all SDK capabilities
- When you need to configure multiple aspects: signals, intervals, attributes, logging

CONFIGURATION DEMONSTRATED:
- All signal types enabled (metrics, logging, tracing)
- Custom export intervals for metrics
- Logging level configuration
- Optional resource attributes (platform, environment)
- Custom attributes via set_attributes()
- Complete production-ready setup
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
    Environment,
    Platform,
    CustomAttributes,
    ExportInterval,
    LoggingLevel,
    SignalTypes
)

# Test data constants
SERVICE_NAME = ServiceName.EXAMPLE_05.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
METRIC_NAME = MetricName.EXAMPLE_05.value
METRIC_VALUE = MetricValue.INCREMENT_BY_ONE.value


def main():
    print_header("Example 5: Complete Initialization",
                 "Initialize with comprehensive configuration")
    
    # Load environment
    _, endpoint, use_console, endpoints = load_environment()
    print_environment_config(endpoint, use_console)
    
    # Initialize SDK operations wrapper
    sdk = SdkOperations(
        endpoint=endpoint,
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Create configuration with all options
    config = sdk.create_configuration(
        endpoint=endpoint,
        use_console=use_console,
        metrics_interval_ms=ExportInterval.METRICS_30S.value,
        logging_level=LoggingLevel.INFO.value
    )
    sdk.apply_signal_specific_endpoints(config, endpoints)
    
    # Create attributes with optional fields
    attrs = sdk.create_attributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION,
        platform=Platform.CONDA.value,
        environment=Environment.DEVELOPMENT.value
    )
    
    # Add custom attributes for this example
    custom_attrs = CustomAttributes.EXAMPLE_COMPLETE.value
    sdk.set_custom_attributes(attrs, **custom_attrs)
    
    # Initialize with all signals
    sdk.initialize(config, attrs, signal_types=SignalTypes.ALL_SIGNALS.value)
    
    # Send a test metric
    sdk.increment_counter(METRIC_NAME, by=METRIC_VALUE)
    
    print_footer("[OK] Example 5 completed successfully!")


if __name__ == "__main__":
    main()
