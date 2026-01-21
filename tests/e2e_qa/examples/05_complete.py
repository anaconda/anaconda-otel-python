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
    
    # Create configuration with all options
    config = Configuration(default_endpoint=endpoint)
    apply_signal_specific_endpoints(config, endpoints)
    if use_console:
        config.set_console_exporter(use_console=True)
    config.set_metrics_export_interval_ms(ExportInterval.METRICS_30S.value)
    config.set_logging_level(LoggingLevel.INFO.value)
    
    print_code("config = Configuration(default_endpoint=endpoint)")
    if use_console:
        print_code("config.set_console_exporter(use_console=True)")
    print_code("config.set_metrics_export_interval_ms(30000)")
    print_code("config.set_logging_level('info')")
    
    # Create attributes with optional fields
    attrs = ResourceAttributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION,
        platform=Platform.CONDA.value,
        environment=Environment.DEVELOPMENT.value
    )
    print_code(f'attrs = ResourceAttributes(service_name="{SERVICE_NAME}", service_version="{SERVICE_VERSION}", platform="conda", environment="development")')
    
    # Add custom attributes for this example
    custom_attrs = CustomAttributes.EXAMPLE_COMPLETE.value
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
    
    print_info("✓ Complete telemetry initialization successful")
    print_info("Configuration:")
    if use_console:
        print_info("  ✓ Console exporter enabled")
    print_info("  ✓ Export interval: 30 seconds")
    print_info("  ✓ Logging level: info")
    print_info("Attributes:")
    print_info(f"  ✓ Service: {SERVICE_NAME} v{SERVICE_VERSION}")
    print_info("  ✓ Platform: conda")
    print_info("  ✓ Environment: development")
    print_info("Signals:")
    print_info("  ✓ Metrics, Logs, Traces")
    
    # Print SDK commands summary
    print_sdk_commands_summary([
        'config = Configuration(default_endpoint=...)',
        'config.set_metrics_export_interval_ms(30000)',
        'config.set_logging_level("info")',
        'attrs = ResourceAttributes(service_name="...", service_version="...", platform="...", environment="...")',
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
    
    print_footer("✓ Example 5 completed successfully!")


if __name__ == "__main__":
    main()
