#!/usr/bin/env python3
"""
Example 1: Initialize All Signals

Demonstrates initializing telemetry with metrics, logs, and traces.
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
SERVICE_NAME = "example-01-all-signals"
SERVICE_VERSION = "1.0.0"
METRIC_NAME = "example_01_initialization_test"
METRIC_VALUE = 1

AUTO_DETECTED_ATTRS = {
    "os.type": "Darwin/Linux/Windows (auto-detected)",
    "python.version": "3.x.x (auto-detected)",
    "client.sdk.version": "0.0.0.devbuild",
    "schema.version": "0.3.0"
}


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
    print_header("Example 1: Initialize All Signals", 
                 "Initialize telemetry with metrics, logs, and traces")
    
    # Load environment
    _, endpoint, use_console = load_environment()
    print_environment_config(endpoint, use_console)
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    # Create attributes
    attrs = ResourceAttributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    print_code(f'attrs = ResourceAttributes(service_name="{SERVICE_NAME}", service_version="{SERVICE_VERSION}")')
    
    # Initialize with all signals
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics', 'logging', 'tracing']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics', 'logging', 'tracing'])")
    
    print_info("✓ Telemetry initialized with all signals")
    print_info("Enabled: metrics, logs, traces")
    
    # Print resource attributes
    print_resource_attributes(attrs)
    
    # Send a test metric
    increment_counter(METRIC_NAME, by=METRIC_VALUE)
    print_metric_info(METRIC_NAME, METRIC_VALUE)
    
    # Print backend validation checklist
    print_backend_validation(SERVICE_NAME, METRIC_NAME, METRIC_VALUE, attrs)
    
    # Flush telemetry
    flush_telemetry()
    
    print_footer("✓ Example 1 completed successfully!")


if __name__ == "__main__":
    main()
