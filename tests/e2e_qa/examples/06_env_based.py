#!/usr/bin/env python3
"""
Example 6: Environment-Based Initialization

Demonstrates initialization based on environment configuration with metric attributes.
This is a standalone script to ensure proper initialization.

WHEN TO USE THIS APPROACH:
- Your application runs in multiple environments (dev, staging, production)
- You need to configure telemetry based on environment variables
- You want to tag telemetry data with environment-specific metadata
- You need different behavior per environment without code changes

USE CASES:
- Multi-environment deployments (dev/staging/production)
- Applications using 12-factor app configuration principles
- Services that need environment-aware telemetry tagging
- Deployments where configuration is managed externally (env vars, config files)
- When you want to track which environment generated specific telemetry data

FEATURES DEMONSTRATED:
- Loading configuration from environment variables
- Setting environment-specific resource attributes
- Adding custom attributes with environment context
- Metric-level attributes for additional environment tagging
- Dynamic configuration based on runtime environment
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
    SignalTypes,
    TestType
)

# Test data constants
SERVICE_NAME = ServiceName.EXAMPLE_06.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
METRIC_NAME = MetricName.EXAMPLE_06.value
METRIC_VALUE = MetricValue.INCREMENT_BY_ONE.value


def main():
    print_header("Example 6: Environment-Based Initialization",
                 "Initialize based on environment configuration")
    
    # Load environment
    otel_env, endpoint, use_console, endpoints = load_environment()
    print_environment_config(endpoint, use_console, otel_env)
    
    # Initialize SDK operations wrapper
    sdk = SdkOperations(
        endpoint=endpoint,
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Create configuration
    config = sdk.create_configuration(endpoint=endpoint, use_console=use_console)
    sdk.apply_signal_specific_endpoints(config, endpoints)
    
    # Create attributes with environment info
    attrs = sdk.create_attributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION,
        environment=Environment.STAGING.value
    )
    
    # Add custom attributes for this example
    custom_attrs = {"otel_environment": otel_env, "test_type": TestType.E2E_QA.value}
    sdk.set_custom_attributes(attrs, **custom_attrs)
    
    # Initialize with all signals
    sdk.initialize(config, attrs, signal_types=SignalTypes.ALL_SIGNALS.value)
    
    # Send a test metric with metric-level attribute
    metric_attrs = {"environment": otel_env}
    sdk.increment_counter(METRIC_NAME, by=METRIC_VALUE, attributes=metric_attrs)
    
    print_footer("✓ Example 6 completed successfully!")


if __name__ == "__main__":
    main()
