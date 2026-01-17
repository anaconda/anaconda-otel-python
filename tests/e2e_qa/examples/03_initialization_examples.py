# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Initialization Examples

This module demonstrates how to initialize the Anaconda OpenTelemetry SDK
with different configurations and signal combinations.
"""

from anaconda.opentelemetry import (
    Configuration,
    ResourceAttributes,
    initialize_telemetry,
    increment_counter
)
from config_utils import (
    load_environment,
    print_example_header,
    print_example_section,
    print_success,
    print_info,
    validate_environment
)


def example_01_initialize_all_signals():
    """Example 1: Initialize with all signals (metrics, logs, traces)"""
    print_example_section("Example 1: Initialize All Signals")
    print_info("Initialize telemetry with metrics, logs, and traces")
    
    # Get endpoint from environment
    _, endpoint, use_console = load_environment()
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    # Create attributes
    attrs = ResourceAttributes(
        service_name="example-01-all-signals",
        service_version="1.0.0"
    )
    
    # Initialize with all signals
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics', 'logging', 'tracing']
    )
    
    print_success("Telemetry initialized with all signals")
    print_info("Enabled: metrics, logs, traces")
    
    # Send a test metric to verify initialization
    increment_counter("example_01_initialization_test", by=1)
    print_info("Test metric sent: example_01_initialization_test")


def example_02_initialize_metrics_only():
    """Example 2: Initialize with metrics only (default)"""
    print_example_section("Example 2: Initialize Metrics Only")
    print_info("Initialize telemetry with only metrics signal")
    
    _, endpoint, use_console = load_environment()
    
    config = Configuration(default_endpoint=endpoint)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    attrs = ResourceAttributes(
        service_name="example-02-metrics-only",
        service_version="1.0.0"
    )
    
    # Initialize with metrics only (default behavior)
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics']
    )
    
    print_success("Telemetry initialized with metrics only")
    print_info("Enabled: metrics")
    
    # Send a test metric
    increment_counter("example_02_metrics_test", by=1)
    print_info("Test metric sent: example_02_metrics_test")


def example_03_initialize_default():
    """Example 3: Initialize with default settings (metrics only)"""
    print_example_section("Example 3: Default Initialization")
    print_info("Initialize with default settings (no signals parameter)")
    
    _, endpoint, use_console = load_environment()
    
    config = Configuration(default_endpoint=endpoint)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    attrs = ResourceAttributes(
        service_name="example-03-default",
        service_version="1.0.0"
    )
    
    # Initialize with default (metrics only)
    initialize_telemetry(config=config, attributes=attrs)
    
    print_success("Telemetry initialized with defaults")
    print_info("Default behavior: metrics signal enabled")
    
    # Send a test metric
    increment_counter("example_03_default_test", by=1)
    print_info("Test metric sent: example_03_default_test")


def example_04_initialize_selective_signals():
    """Example 4: Initialize with selective signals"""
    print_example_section("Example 4: Selective Signals")
    print_info("Initialize with only specific signals needed")
    
    _, endpoint, use_console = load_environment()
    
    config = Configuration(default_endpoint=endpoint)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    attrs = ResourceAttributes(
        service_name="example-04-selective",
        service_version="1.0.0"
    )
    
    # Initialize with metrics and traces only (no logs)
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics', 'tracing']
    )
    
    print_success("Telemetry initialized with selective signals")
    print_info("Enabled: metrics, traces")
    print_info("Disabled: logs")
    
    # Send a test metric
    increment_counter("example_04_selective_test", by=1)
    print_info("Test metric sent: example_04_selective_test")


def example_05_complete_initialization():
    """Example 5: Complete initialization with all configuration options"""
    print_example_section("Example 5: Complete Initialization")
    print_info("Initialize with comprehensive configuration")
    
    _, endpoint, use_console = load_environment()
    
    # Create comprehensive configuration
    config = Configuration(default_endpoint=endpoint)
    config.set_console_exporter(use_console=True)
    config.set_metrics_export_interval_ms(30000)  # 30 seconds
    config.set_logging_level('info')
    config.set_skip_internet_check(False)
    
    # Create comprehensive attributes
    attrs = ResourceAttributes(
        service_name="example-05-complete",
        service_version="1.0.0",
        platform="conda",
        environment="development"
    )
    
    # Add custom attributes
    attrs.set_attributes(
        example="complete_initialization",
        test_type="e2e-qa"
    )
    
    # Initialize with all signals
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics', 'logging', 'tracing']
    )
    
    print_success("Complete telemetry initialization successful")
    print_info("Configuration:")
    print_info("  ✓ Console exporter enabled")
    print_info("  ✓ Export interval: 30 seconds")
    print_info("  ✓ Logging level: info")
    print_info("Attributes:")
    print_info(f"  ✓ Service: {attrs.service_name} v{attrs.service_version}")
    print_info(f"  ✓ Platform: {attrs.platform}")
    print_info(f"  ✓ Environment: {attrs.environment}")
    print_info("Signals:")
    print_info("  ✓ Metrics, Logs, Traces")
    
    # Send a test metric
    increment_counter("example_05_complete_test", by=1)
    print_info("Test metric sent: example_05_complete_test")


def example_06_environment_based_initialization():
    """Example 6: Environment-based initialization"""
    print_example_section("Example 6: Environment-Based Initialization")
    print_info("Initialize based on environment configuration")
    
    env_name, endpoint, use_console = load_environment()
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    # Map environment name to valid ResourceAttributes environment value
    env_mapping = {
        'staging-internal': 'staging',
        'staging-public': 'staging',
        'production-external': 'production',
        'production-internal': 'production',
    }
    environment = env_mapping.get(env_name, 'development')
    
    # Create attributes with environment info
    attrs = ResourceAttributes(
        service_name="example-06-env-based",
        service_version="1.0.0",
        environment=environment
    )
    
    attrs.set_attributes(
        otel_environment=env_name,
        test_type="e2e-qa"
    )
    
    # Initialize
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics', 'logging', 'tracing']
    )
    
    print_success("Environment-based initialization successful")
    print_info(f"OTEL Environment: {env_name}")
    print_info(f"Endpoint: {endpoint}")
    print_info(f"Service Environment: {attrs.environment}")
    
    # Send a test metric
    increment_counter("example_06_env_based_test", by=1, attributes={"environment": env_name})
    print_info(f"Test metric sent with environment tag: {env_name}")


def run_all_examples():
    """Run all initialization examples"""
    print_example_header(
        "Initialization Examples",
        "Demonstrating initialize_telemetry() with different configurations"
    )
    
    # Validate environment
    validate_environment()
    
    print("\n⚠️  Note: Each example initializes telemetry independently.")
    print("    In a real application, you would only initialize once.\n")
    
    # Run examples
    example_01_initialize_all_signals()
    print_info("\nWaiting before next initialization...\n")
    
    example_02_initialize_metrics_only()
    print_info("\nWaiting before next initialization...\n")
    
    example_03_initialize_default()
    print_info("\nWaiting before next initialization...\n")
    
    example_04_initialize_selective_signals()
    print_info("\nWaiting before next initialization...\n")
    
    example_05_complete_initialization()
    print_info("\nWaiting before next initialization...\n")
    
    example_06_environment_based_initialization()
    
    print("\n" + "=" * 70)
    print_success("All initialization examples completed!")
    print_info("Note: Check console output above for telemetry data")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_all_examples()
