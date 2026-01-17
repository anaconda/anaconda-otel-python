#!/usr/bin/env python3
"""
Example 2: Initialize Metrics Only

Demonstrates initializing telemetry with only the metrics signal.
This is a standalone script to ensure proper initialization.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

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
    flush_telemetry
)

# Test data constants
SERVICE_NAME = "example-02-metrics-only"
SERVICE_VERSION = "1.0.0"
METRIC_NAME = "example_02_metrics_test"
METRIC_VALUE = 1

AUTO_DETECTED_ATTRS = {
    "os.type": "Darwin/Linux/Windows (auto-detected)",
    "python.version": "3.x.x (auto-detected)",
    "client.sdk.version": "0.0.0.devbuild",
    "schema.version": "0.3.0"
}


def main():
    print_header("Example 2: Initialize Metrics Only",
                 "Initialize telemetry with only metrics signal")
    
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
    
    # Initialize with metrics only
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics'])")
    
    print_info("✓ Telemetry initialized with metrics only")
    print_info("Enabled: metrics")
    
    # Print resource attributes
    print_resource_attributes(attrs)
    
    # Send a test metric
    increment_counter(METRIC_NAME, by=METRIC_VALUE)
    print_metric_info(METRIC_NAME, METRIC_VALUE)
    
    # Print backend validation checklist
    print_backend_validation(SERVICE_NAME, METRIC_NAME, METRIC_VALUE, attrs)
    
    # Flush telemetry
    flush_telemetry()
    
    print_footer("✓ Example 2 completed successfully!")


if __name__ == "__main__":
    main()
