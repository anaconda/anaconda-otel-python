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
from opentelemetry import metrics
from config_utils import load_environment, print_code, print_validation_info

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


def flush_telemetry():
    """Force flush all telemetry data to ensure it's sent to the backend."""
    try:
        meter_provider = metrics.get_meter_provider()
        if hasattr(meter_provider, 'force_flush'):
            meter_provider.force_flush(timeout_millis=5000)
        print("  ✓ Telemetry flushed to backend")
    except Exception as e:
        print(f"  ⚠️  Warning: Error during flush: {e}")


def main():
    print("\n" + "=" * 70)
    print("  Example 2: Initialize Metrics Only")
    print("=" * 70)
    print("  Initialize telemetry with only metrics signal")
    print("-" * 70)
    
    # Load environment
    _, endpoint, use_console = load_environment()
    print(f"  Endpoint: {endpoint}")
    print(f"  Console Exporter: {use_console}")
    
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
    
    print("  ✓ Telemetry initialized with metrics only")
    print("  Enabled: metrics")
    
    # Print resource attributes
    print("\n  📋 Resource Attributes (sent with every metric):")
    print(f"     • service.name: {attrs.service_name}")
    print(f"     • service.version: {attrs.service_version}")
    print(f"     • os.type: {attrs.os_type}")
    print(f"     • os.version: {attrs.os_version}")
    print(f"     • python.version: {attrs.python_version}")
    print(f"     • hostname: {attrs.hostname}")
    print(f"     • platform: {attrs.platform if attrs.platform else '(empty)'}")
    print(f"     • environment: {attrs.environment if attrs.environment else '(empty)'}")
    print(f"     • client.sdk.version: {attrs.client_sdk_version}")
    print(f"     • schema.version: {attrs.schema_version}")
    print(f"     • session.id: (auto-generated, visible with console exporter)")
    if attrs.parameters:
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
    print(f"       • os.type: {attrs.os_type}")
    print(f"       • python.version: {attrs.python_version}")
    print(f"       • client.sdk.version: {attrs.client_sdk_version}")
    print(f"       • schema.version: {attrs.schema_version}")
    
    # Flush telemetry
    print("\n  Flushing telemetry data...")
    flush_telemetry()
    
    print("\n" + "=" * 70)
    print("  ✓ Example 2 completed successfully!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
