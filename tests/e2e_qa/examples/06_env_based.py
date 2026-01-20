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

from anaconda.opentelemetry import Configuration, ResourceAttributes, initialize_telemetry, increment_counter
from utils import (
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
    flush_telemetry
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
    otel_env, endpoint, use_console = load_environment()
    print_environment_config(endpoint, use_console, otel_env)
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    # Create attributes with environment info
    attrs = ResourceAttributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION,
        environment=Environment.STAGING.value
    )
    attrs.set_attributes(otel_environment=otel_env, test_type=TestType.E2E_QA.value)
    
    print_code(f'attrs = ResourceAttributes(service_name="{SERVICE_NAME}", service_version="{SERVICE_VERSION}", environment="staging")')
    print_code(f'attrs.set_attributes(otel_environment="{otel_env}", test_type="e2e-qa")')
    
    # Initialize with all signals
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=SignalTypes.ALL_SIGNALS.value
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics', 'logging', 'tracing'])")
    
    print_info("✓ Environment-based initialization successful")
    print_info(f"OTEL Environment: {otel_env}")
    print_info(f"Endpoint: {endpoint}")
    print_info("Service Environment: staging")
    
    # Print SDK commands summary
    print_sdk_commands_summary([
        'config = Configuration(default_endpoint=...)',
        'attrs = ResourceAttributes(service_name="...", service_version="...", environment="staging")',
        'attrs.set_attributes(otel_environment="staging-internal", test_type="e2e-qa")',
        "initialize_telemetry(config, attrs, signal_types=['metrics', 'logging', 'tracing'])",
        'increment_counter("example_06_env_based_test", by=1, attributes={"environment": "staging-internal"})',
    ])
    
    # Print resource attributes
    print_resource_attributes(attrs)
    
    # Send a test metric with metric-level attribute
    metric_attrs = {"environment": otel_env}
    increment_counter(METRIC_NAME, by=METRIC_VALUE, attributes=metric_attrs)
    print_metric_info(METRIC_NAME, METRIC_VALUE, metric_attrs)
    
    # Print backend validation checklist
    print_backend_validation(SERVICE_NAME, METRIC_NAME, METRIC_VALUE, attrs, metric_attrs)
    
    # Flush telemetry
    flush_telemetry()
    
    print_footer("✓ Example 6 completed successfully!")


if __name__ == "__main__":
    main()
