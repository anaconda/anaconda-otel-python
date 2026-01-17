#!/usr/bin/env python3
"""
Example 6: Environment-Based Initialization

Demonstrates initialization based on environment configuration with metric attributes.
This is a standalone script to ensure proper initialization.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from anaconda.opentelemetry import Configuration, ResourceAttributes, initialize_telemetry, increment_counter
from opentelemetry import metrics, trace
from anaconda.opentelemetry.signals import _AnacondaLogger
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
    print_flush_status
)

# Test data constants
SERVICE_NAME = "example-06-env-based"
SERVICE_VERSION = "1.0.0"
METRIC_NAME = "example_06_env_based_test"
METRIC_VALUE = 1


def flush_telemetry():
    """Force flush all telemetry data to ensure it's sent to the backend."""
    try:
        meter_provider = metrics.get_meter_provider()
        if hasattr(meter_provider, 'force_flush'):
            meter_provider.force_flush(timeout_millis=5000)
        
        tracer_provider = trace.get_tracer_provider()
        if hasattr(tracer_provider, 'force_flush'):
            tracer_provider.force_flush(timeout_millis=5000)
        
        if _AnacondaLogger._instance:
            logger_instance = _AnacondaLogger._instance
            if hasattr(logger_instance, '_provider') and logger_instance._provider:
                logger_instance._provider.force_flush(timeout_millis=5000)
        
        print_flush_status(success=True)
    except Exception as e:
        print_flush_status(success=False, error=e)


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
        environment="staging"
    )
    attrs.set_attributes(otel_environment=otel_env, test_type="e2e-qa")
    
    print_code(f'attrs = ResourceAttributes(service_name="{SERVICE_NAME}", service_version="{SERVICE_VERSION}", environment="staging")')
    print_code(f'attrs.set_attributes(otel_environment="{otel_env}", test_type="e2e-qa")')
    
    # Initialize with all signals
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics', 'logging', 'tracing']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics', 'logging', 'tracing'])")
    
    print_info("✓ Environment-based initialization successful")
    print_info(f"OTEL Environment: {otel_env}")
    print_info(f"Endpoint: {endpoint}")
    print_info("Service Environment: staging")
    
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
