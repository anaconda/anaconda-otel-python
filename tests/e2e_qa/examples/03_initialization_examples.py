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
    print_code,
    print_validation_info,
    get_session_id,
    validate_environment
)

# Import OpenTelemetry providers for flushing
from opentelemetry import metrics, trace
from anaconda.opentelemetry.signals import _AnacondaLogger


# ============================================================================
# Helper Functions
# ============================================================================

def flush_telemetry():
    """
    Force flush all telemetry data to ensure it's sent to the backend.
    This is critical for short-lived programs to ensure data is exported.
    """
    try:
        # Flush metrics
        meter_provider = metrics.get_meter_provider()
        if hasattr(meter_provider, 'force_flush'):
            meter_provider.force_flush(timeout_millis=5000)
        
        # Flush traces
        tracer_provider = trace.get_tracer_provider()
        if hasattr(tracer_provider, 'force_flush'):
            tracer_provider.force_flush(timeout_millis=5000)
        
        # Flush logs
        if _AnacondaLogger._instance:
            logger_instance = _AnacondaLogger._instance
            if hasattr(logger_instance, '_provider') and logger_instance._provider:
                logger_instance._provider.force_flush(timeout_millis=5000)
    except Exception as e:
        print(f"  ⚠️  Warning: Error during flush: {e}")


# ============================================================================
# Test Data Constants
# ============================================================================

# Example 1: Initialize All Signals
EXAMPLE_01_SERVICE_NAME = "example-01-all-signals"
EXAMPLE_01_SERVICE_VERSION = "1.0.0"
EXAMPLE_01_METRIC_NAME = "example_01_initialization_test"
EXAMPLE_01_METRIC_VALUE = 1

# Example 2: Initialize Metrics Only
EXAMPLE_02_SERVICE_NAME = "example-02-metrics-only"
EXAMPLE_02_SERVICE_VERSION = "1.0.0"
EXAMPLE_02_METRIC_NAME = "example_02_metrics_test"
EXAMPLE_02_METRIC_VALUE = 1

# Example 3: Default Initialization
EXAMPLE_03_SERVICE_NAME = "example-03-default"
EXAMPLE_03_SERVICE_VERSION = "1.0.0"
EXAMPLE_03_METRIC_NAME = "example_03_default_test"
EXAMPLE_03_METRIC_VALUE = 1

# Example 4: Selective Signals
EXAMPLE_04_SERVICE_NAME = "example-04-selective"
EXAMPLE_04_SERVICE_VERSION = "1.0.0"
EXAMPLE_04_METRIC_NAME = "example_04_selective_test"
EXAMPLE_04_METRIC_VALUE = 1

# Example 5: Complete Initialization
EXAMPLE_05_SERVICE_NAME = "example-05-complete"
EXAMPLE_05_SERVICE_VERSION = "1.0.0"
EXAMPLE_05_PLATFORM = "conda"
EXAMPLE_05_ENVIRONMENT = "development"
EXAMPLE_05_METRIC_NAME = "example_05_complete_test"
EXAMPLE_05_METRIC_VALUE = 1
EXAMPLE_05_CUSTOM_ATTRS = {
    "example": "complete_initialization",
    "test_type": "e2e-qa"
}

# Example 6: Environment-Based Initialization
EXAMPLE_06_SERVICE_NAME = "example-06-env-based"
EXAMPLE_06_SERVICE_VERSION = "1.0.0"
EXAMPLE_06_METRIC_NAME = "example_06_env_based_test"
EXAMPLE_06_METRIC_VALUE = 1

# Common resource attributes (auto-detected)
AUTO_DETECTED_ATTRS = {
    "os.type": "Darwin/Linux/Windows (auto-detected)",
    "python.version": "3.x.x (auto-detected)",
    "client.sdk.version": "0.0.0.devbuild",
    "schema.version": "0.3.0"
}


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
        service_name=EXAMPLE_01_SERVICE_NAME,
        service_version=EXAMPLE_01_SERVICE_VERSION
    )
    print_code(f'attrs = ResourceAttributes(service_name="{EXAMPLE_01_SERVICE_NAME}", service_version="{EXAMPLE_01_SERVICE_VERSION}")')
    
    # Initialize with all signals
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics', 'logging', 'tracing']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics', 'logging', 'tracing'])")
    
    print_success("Telemetry initialized with all signals")
    print_info("Enabled: metrics, logs, traces")
    
    # Get session ID
    session_id = get_session_id(attrs)
    if session_id:
        print_info(f"Session ID: {session_id}")
    
    # Send a test metric to verify initialization
    increment_counter(EXAMPLE_01_METRIC_NAME, by=EXAMPLE_01_METRIC_VALUE)
    print_code(f'increment_counter("{EXAMPLE_01_METRIC_NAME}", by={EXAMPLE_01_METRIC_VALUE})')
    print_validation_info(
        metric_name=EXAMPLE_01_METRIC_NAME,
        value=EXAMPLE_01_METRIC_VALUE,
        service_name=EXAMPLE_01_SERVICE_NAME,
        resource_attrs={
            "service.version": EXAMPLE_01_SERVICE_VERSION,
            **AUTO_DETECTED_ATTRS
        },
        session_id=session_id
    )


def example_02_initialize_metrics_only():
    """Example 2: Initialize with metrics only (default)"""
    print_example_section("Example 2: Initialize Metrics Only")
    print_info("Initialize telemetry with only metrics signal")
    
    _, endpoint, use_console = load_environment()
    
    config = Configuration(default_endpoint=endpoint)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    attrs = ResourceAttributes(
        service_name=EXAMPLE_02_SERVICE_NAME,
        service_version=EXAMPLE_02_SERVICE_VERSION
    )
    print_code(f'attrs = ResourceAttributes(service_name="{EXAMPLE_02_SERVICE_NAME}", service_version="{EXAMPLE_02_SERVICE_VERSION}")')
    
    # Initialize with metrics only (default behavior)
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics'])")
    
    print_success("Telemetry initialized with metrics only")
    print_info("Enabled: metrics")
    
    # Get session ID
    session_id = get_session_id(attrs)
    if session_id:
        print_info(f"Session ID: {session_id}")
    
    # Send a test metric
    increment_counter(EXAMPLE_02_METRIC_NAME, by=EXAMPLE_02_METRIC_VALUE)
    print_code(f'increment_counter("{EXAMPLE_02_METRIC_NAME}", by={EXAMPLE_02_METRIC_VALUE})')
    print_validation_info(
        metric_name=EXAMPLE_02_METRIC_NAME,
        value=EXAMPLE_02_METRIC_VALUE,
        service_name=EXAMPLE_02_SERVICE_NAME,
        resource_attrs={
            "service.version": EXAMPLE_02_SERVICE_VERSION
        },
        session_id=session_id
    )


def example_03_initialize_default():
    """Example 3: Initialize with default settings (metrics only)"""
    print_example_section("Example 3: Default Initialization")
    print_info("Initialize with default settings (no signals parameter)")
    
    _, endpoint, use_console = load_environment()
    
    config = Configuration(default_endpoint=endpoint)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    attrs = ResourceAttributes(
        service_name=EXAMPLE_03_SERVICE_NAME,
        service_version=EXAMPLE_03_SERVICE_VERSION
    )
    print_code(f'attrs = ResourceAttributes(service_name="{EXAMPLE_03_SERVICE_NAME}", service_version="{EXAMPLE_03_SERVICE_VERSION}")')
    
    # Initialize with default (metrics only)
    initialize_telemetry(config=config, attributes=attrs)
    print_code("initialize_telemetry(config, attrs)  # No signal_types = defaults to metrics")
    
    print_success("Telemetry initialized with defaults")
    print_info("Default behavior: metrics signal enabled")
    
    # Get session ID
    session_id = get_session_id(attrs)
    if session_id:
        print_info(f"Session ID: {session_id}")
    
    # Send a test metric
    increment_counter(EXAMPLE_03_METRIC_NAME, by=EXAMPLE_03_METRIC_VALUE)
    print_code(f'increment_counter("{EXAMPLE_03_METRIC_NAME}", by={EXAMPLE_03_METRIC_VALUE})')
    print_validation_info(
        metric_name=EXAMPLE_03_METRIC_NAME,
        value=EXAMPLE_03_METRIC_VALUE,
        service_name=EXAMPLE_03_SERVICE_NAME,
        resource_attrs={
            "service.version": EXAMPLE_03_SERVICE_VERSION
        },
        session_id=session_id
    )


def example_04_initialize_selective_signals():
    """Example 4: Initialize with selective signals"""
    print_example_section("Example 4: Selective Signals")
    print_info("Initialize with only specific signals needed")
    
    _, endpoint, use_console = load_environment()
    
    config = Configuration(default_endpoint=endpoint)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    attrs = ResourceAttributes(
        service_name=EXAMPLE_04_SERVICE_NAME,
        service_version=EXAMPLE_04_SERVICE_VERSION
    )
    print_code(f'attrs = ResourceAttributes(service_name="{EXAMPLE_04_SERVICE_NAME}", service_version="{EXAMPLE_04_SERVICE_VERSION}")')
    
    # Initialize with metrics and traces only (no logs)
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics', 'tracing']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics', 'tracing'])")
    
    print_success("Telemetry initialized with selective signals")
    print_info("Enabled: metrics, traces")
    print_info("Disabled: logs")
    
    # Get session ID
    session_id = get_session_id(attrs)
    if session_id:
        print_info(f"Session ID: {session_id}")
    
    # Send a test metric
    increment_counter(EXAMPLE_04_METRIC_NAME, by=EXAMPLE_04_METRIC_VALUE)
    print_code(f'increment_counter("{EXAMPLE_04_METRIC_NAME}", by={EXAMPLE_04_METRIC_VALUE})')
    print_validation_info(
        metric_name=EXAMPLE_04_METRIC_NAME,
        value=EXAMPLE_04_METRIC_VALUE,
        service_name=EXAMPLE_04_SERVICE_NAME,
        resource_attrs={
            "service.version": EXAMPLE_04_SERVICE_VERSION
        },
        session_id=session_id
    )


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
    print_code('config = Configuration(default_endpoint=endpoint)')
    print_code('config.set_console_exporter(use_console=True)')
    print_code('config.set_metrics_export_interval_ms(30000)')
    print_code("config.set_logging_level('info')")
    
    # Create comprehensive attributes
    attrs = ResourceAttributes(
        service_name=EXAMPLE_05_SERVICE_NAME,
        service_version=EXAMPLE_05_SERVICE_VERSION,
        platform=EXAMPLE_05_PLATFORM,
        environment=EXAMPLE_05_ENVIRONMENT
    )
    print_code(f'attrs = ResourceAttributes(service_name="{EXAMPLE_05_SERVICE_NAME}", service_version="{EXAMPLE_05_SERVICE_VERSION}", platform="{EXAMPLE_05_PLATFORM}", environment="{EXAMPLE_05_ENVIRONMENT}")')
    
    # Add custom attributes
    attrs.set_attributes(**EXAMPLE_05_CUSTOM_ATTRS)
    custom_attrs_str = ", ".join([f'{k}="{v}"' for k, v in EXAMPLE_05_CUSTOM_ATTRS.items()])
    print_code(f'attrs.set_attributes({custom_attrs_str})')
    
    # Initialize with all signals
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics', 'logging', 'tracing']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics', 'logging', 'tracing'])")
    
    print_success("Complete telemetry initialization successful")
    print_info("Configuration:")
    print_info("  ✓ Console exporter enabled")
    print_info("  ✓ Export interval: 30 seconds")
    print_info("  ✓ Logging level: info")
    print_info("Attributes:")
    print_info(f"  ✓ Service: {EXAMPLE_05_SERVICE_NAME} v{EXAMPLE_05_SERVICE_VERSION}")
    print_info(f"  ✓ Platform: {EXAMPLE_05_PLATFORM}")
    print_info(f"  ✓ Environment: {EXAMPLE_05_ENVIRONMENT}")
    print_info("Signals:")
    print_info("  ✓ Metrics, Logs, Traces")
    
    # Get session ID
    session_id = get_session_id(attrs)
    if session_id:
        print_info(f"Session ID: {session_id}")
    
    # Send a test metric
    increment_counter(EXAMPLE_05_METRIC_NAME, by=EXAMPLE_05_METRIC_VALUE)
    print_code(f'increment_counter("{EXAMPLE_05_METRIC_NAME}", by={EXAMPLE_05_METRIC_VALUE})')
    
    import json
    params_json = json.dumps(EXAMPLE_05_CUSTOM_ATTRS)
    print_validation_info(
        metric_name=EXAMPLE_05_METRIC_NAME,
        value=EXAMPLE_05_METRIC_VALUE,
        service_name=EXAMPLE_05_SERVICE_NAME,
        resource_attrs={
            "service.version": EXAMPLE_05_SERVICE_VERSION,
            "platform": EXAMPLE_05_PLATFORM,
            "environment": EXAMPLE_05_ENVIRONMENT,
            "parameters": params_json
        },
        session_id=session_id
    )


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
        service_name=EXAMPLE_06_SERVICE_NAME,
        service_version=EXAMPLE_06_SERVICE_VERSION,
        environment=environment
    )
    print_code(f'attrs = ResourceAttributes(service_name="{EXAMPLE_06_SERVICE_NAME}", service_version="{EXAMPLE_06_SERVICE_VERSION}", environment="{environment}")')
    
    custom_attrs = {
        "otel_environment": env_name,
        "test_type": "e2e-qa"
    }
    attrs.set_attributes(**custom_attrs)
    print_code(f'attrs.set_attributes(otel_environment="{env_name}", test_type="e2e-qa")')
    
    # Initialize
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics', 'logging', 'tracing']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics', 'logging', 'tracing'])")
    
    print_success("Environment-based initialization successful")
    print_info(f"OTEL Environment: {env_name}")
    print_info(f"Endpoint: {endpoint}")
    print_info(f"Service Environment: {environment}")
    
    # Get session ID
    session_id = get_session_id(attrs)
    if session_id:
        print_info(f"Session ID: {session_id}")
    
    # Send a test metric
    metric_attrs = {"environment": env_name}
    increment_counter(EXAMPLE_06_METRIC_NAME, by=EXAMPLE_06_METRIC_VALUE, attributes=metric_attrs)
    print_code(f'increment_counter("{EXAMPLE_06_METRIC_NAME}", by={EXAMPLE_06_METRIC_VALUE}, attributes={{"environment": "{env_name}"}})')
    
    import json
    params_json = json.dumps(custom_attrs)
    print_validation_info(
        metric_name=EXAMPLE_06_METRIC_NAME,
        value=EXAMPLE_06_METRIC_VALUE,
        attributes=metric_attrs,
        service_name=EXAMPLE_06_SERVICE_NAME,
        resource_attrs={
            "service.version": EXAMPLE_06_SERVICE_VERSION,
            "environment": environment,
            "parameters": params_json
        },
        session_id=session_id
    )


def run_all_examples():
    """Run all initialization examples"""
    print_example_header(
        "Initialization Examples",
        "Demonstrating initialize_telemetry() with different configurations"
    )
    
    # Validate environment
    validate_environment()
    
    print("\n⚠️  Note: Each example initializes telemetry independently.")
    print("    In a real application, you would only initialize once.")
    print("\n📋 Session ID: Will be shown in console JSON output at the end.")
    print("    Look for 'session.id' in the resource attributes.\n")
    
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
    
    # CRITICAL: Flush all telemetry data to backend
    print_info("Flushing all telemetry data to backend...")
    flush_telemetry()
    print_success("✓ All telemetry data flushed to backend")
    print_info("Note: Check console output above for telemetry data")
    print("\n" + "=" * 70)
    print("📋 BACKEND VALIDATION SUMMARY")
    print("=" * 70)
    
    # Check if console exporter is enabled
    _, _, use_console = load_environment()
    if use_console:
        print("\n⚠️  CRITICAL WARNING:")
        print("   OTEL_CONSOLE_EXPORTER=true in .env")
        print("   Data is ONLY printed to console, NOT sent to backend!")
        print("   To validate in backend: Set OTEL_CONSOLE_EXPORTER=false")
        print("=" * 70)
    
    print("\n🔑 Session ID:")
    print("   All metrics in this test run share the same session ID.")
    if use_console:
        print("   Look for 'session.id' in the console JSON output below.")
    else:
        print("   Session ID is generated but not visible without console exporter.")
        print("   Query backend for metrics by service name or time range.")
    print("   Use this session ID to query the backend for all 6 test metrics.")
    print("\n📊 Metrics Sent:")
    print(f"   1. {EXAMPLE_01_METRIC_NAME} (service: {EXAMPLE_01_SERVICE_NAME})")
    print(f"   2. {EXAMPLE_02_METRIC_NAME} (service: {EXAMPLE_02_SERVICE_NAME})")
    print(f"   3. {EXAMPLE_03_METRIC_NAME} (service: {EXAMPLE_03_SERVICE_NAME})")
    print(f"   4. {EXAMPLE_04_METRIC_NAME} (service: {EXAMPLE_04_SERVICE_NAME})")
    print(f"   5. {EXAMPLE_05_METRIC_NAME} (service: {EXAMPLE_05_SERVICE_NAME})")
    print(f"   6. {EXAMPLE_06_METRIC_NAME} (service: {EXAMPLE_06_SERVICE_NAME})")
    print("\n💡 To validate in backend:")
    print("   1. Extract session.id from JSON output below")
    print("   2. Query backend: SELECT * FROM metrics WHERE session_id = '<session.id>'")
    print("   3. Verify all 6 metrics are present with correct values")
    print("=" * 70 + "\n")
    
    # Add a small delay to ensure console exporter output appears
    import time
    time.sleep(1)


if __name__ == "__main__":
    run_all_examples()
