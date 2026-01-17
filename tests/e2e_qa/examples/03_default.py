#!/usr/bin/env python3
"""
Example 3: Default Initialization

Demonstrates initializing telemetry with default settings (metrics only).
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
from test_data import ServiceName, ServiceVersion, MetricName, MetricValue

# Test data constants
SERVICE_NAME = ServiceName.EXAMPLE_03.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
METRIC_NAME = MetricName.EXAMPLE_03.value
METRIC_VALUE = MetricValue.INCREMENT_BY_ONE.value


def main():
    print_header("Example 3: Default Initialization",
                 "Initialize with default settings (no signals parameter)")
    
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
    
    # Initialize with default (metrics only)
    initialize_telemetry(
        config=config,
        attributes=attrs
    )
    print_code("initialize_telemetry(config, attrs)  # No signal_types = defaults to metrics")
    
    print_info("✓ Telemetry initialized with defaults")
    print_info("Default behavior: metrics signal enabled")
    
    # Print resource attributes
    print_resource_attributes(attrs)
    
    # Send a test metric
    increment_counter(METRIC_NAME, by=METRIC_VALUE)
    print_metric_info(METRIC_NAME, METRIC_VALUE)
    
    # Print backend validation checklist
    print_backend_validation(SERVICE_NAME, METRIC_NAME, METRIC_VALUE, attrs)
    
    # Flush telemetry
    flush_telemetry()
    
    print_footer("✓ Example 3 completed successfully!")


if __name__ == "__main__":
    main()
