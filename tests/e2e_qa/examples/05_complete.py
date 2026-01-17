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
from opentelemetry import metrics, trace
from anaconda.opentelemetry.signals import _AnacondaLogger
from config_utils import load_environment, print_code

# Test data constants
SERVICE_NAME = "example-05-complete"
SERVICE_VERSION = "1.0.0"
METRIC_NAME = "example_05_complete_test"
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
        
        print("  ✓ Telemetry flushed to backend")
    except Exception as e:
        print(f"  ⚠️  Warning: Error during flush: {e}")


def main():
    print("\n" + "=" * 70)
    print("  Example 5: Complete Initialization")
    print("=" * 70)
    print("  Initialize with comprehensive configuration")
    print("-" * 70)
    
    # Load environment
    _, endpoint, use_console = load_environment()
    print(f"  Endpoint: {endpoint}")
    print(f"  Console Exporter: {use_console}")
    
    # Create configuration with all options
    config = Configuration(default_endpoint=endpoint)
    if use_console:
        config.set_console_exporter(use_console=True)
    config.set_metrics_export_interval_ms(30000)
    config.set_logging_level('info')
    
    print_code("config = Configuration(default_endpoint=endpoint)")
    if use_console:
        print_code("config.set_console_exporter(use_console=True)")
    print_code("config.set_metrics_export_interval_ms(30000)")
    print_code("config.set_logging_level('info')")
    
    # Create attributes with optional fields
    attrs = ResourceAttributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION,
        platform="conda",
        environment="development"
    )
    attrs.set_attributes(example="complete_initialization", test_type="e2e-qa")
    
    print_code(f'attrs = ResourceAttributes(service_name="{SERVICE_NAME}", service_version="{SERVICE_VERSION}", platform="conda", environment="development")')
    print_code('attrs.set_attributes(example="complete_initialization", test_type="e2e-qa")')
    
    # Initialize with all signals
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics', 'logging', 'tracing']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics', 'logging', 'tracing'])")
    
    print("  ✓ Complete telemetry initialization successful")
    print("  Configuration:")
    if use_console:
        print("    ✓ Console exporter enabled")
    print("    ✓ Export interval: 30 seconds")
    print("    ✓ Logging level: info")
    print("  Attributes:")
    print(f"    ✓ Service: {SERVICE_NAME} v{SERVICE_VERSION}")
    print("    ✓ Platform: conda")
    print("    ✓ Environment: development")
    print("  Signals:")
    print("    ✓ Metrics, Logs, Traces")
    
    # Print resource attributes
    print("\n  📋 Resource Attributes (sent with every metric):")
    print(f"     • service.name: {attrs.service_name}")
    print(f"     • service.version: {attrs.service_version}")
    print(f"     • os.type: {attrs.os_type}")
    print(f"     • os.version: {attrs.os_version}")
    print(f"     • python.version: {attrs.python_version}")
    print(f"     • hostname: {attrs.hostname}")
    print(f"     • platform: {attrs.platform}")
    print(f"     • environment: {attrs.environment}")
    print(f"     • client.sdk.version: {attrs.client_sdk_version}")
    print(f"     • schema.version: {attrs.schema_version}")
    print(f"     • session.id: (auto-generated, visible with console exporter)")
    print(f"     • parameters: {attrs.parameters}")
    
    # Send a test metric
    print("\n  📊 Sending Metric:")
    increment_counter(METRIC_NAME, by=METRIC_VALUE)
    print_code(f'increment_counter("{METRIC_NAME}", by={METRIC_VALUE})')
    
    # Print backend validation checklist
    print("\n  ✅ BACKEND VALIDATION CHECKLIST:")
    print("     Query backend for this service:")
    print(f"       WHERE service.name = '{SERVICE_NAME}'")
    print(f"       AND timestamp >= NOW() - INTERVAL '10 minutes'")
    print("\n     Expected in backend:")
    print(f"       • Metric Name: {METRIC_NAME}")
    print(f"       • Metric Value: {METRIC_VALUE}")
    print(f"       • service.name: {SERVICE_NAME}")
    print(f"       • service.version: {SERVICE_VERSION}")
    print(f"       • platform: conda")
    print(f"       • environment: development")
    print(f"       • parameters: {attrs.parameters}")
    
    # Flush telemetry
    print("\n  Flushing telemetry data...")
    flush_telemetry()
    
    print("\n" + "=" * 70)
    print("  ✓ Example 5 completed successfully!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
