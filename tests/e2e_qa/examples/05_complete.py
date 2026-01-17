#!/usr/bin/env python3
"""
Example 5: Complete Initialization

Demonstrates comprehensive initialization with all configuration options.
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
    _, endpoint, use_console = load_environment()
    print_environment_config(endpoint, use_console)
    
    # Create configuration with all options
    config = Configuration(default_endpoint=endpoint)
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
    attrs.set_attributes(**CustomAttributes.EXAMPLE_COMPLETE.value)
    
    print_code(f'attrs = ResourceAttributes(service_name="{SERVICE_NAME}", service_version="{SERVICE_VERSION}", platform="conda", environment="development")')
    print_code('attrs.set_attributes(example="complete_initialization", test_type="e2e-qa")')
    
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
    
    # Print resource attributes
    print_resource_attributes(attrs)
    
    # Send a test metric
    increment_counter(METRIC_NAME, by=METRIC_VALUE)
    print_metric_info(METRIC_NAME, METRIC_VALUE)
    
    # Print backend validation checklist
    print_backend_validation(SERVICE_NAME, METRIC_NAME, METRIC_VALUE, attrs)
    
    # Flush telemetry
    flush_telemetry()
    
    print_footer("✓ Example 5 completed successfully!")


if __name__ == "__main__":
    main()
