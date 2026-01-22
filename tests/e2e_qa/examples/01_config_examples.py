#!/usr/bin/env python3
"""
Configuration Examples

This module demonstrates how to create and configure Configuration objects
for the Anaconda OpenTelemetry SDK.
"""

from utils import (
    EndpointType,
    load_environment,
    print_example_header,
    print_example_section,
    print_success,
    print_info,
    validate_environment,
    SdkOperations
)
from test_data import ExportInterval, LoggingLevel


def example_01_basic_configuration():
    """Example 1: Create basic configuration with default endpoint"""
    print_example_section("Example 1: Basic Configuration")
    print_info("Create a Configuration with a default endpoint")
    
    # Get endpoint from environment
    _, endpoint, _, endpoints = load_environment()
    
    # Create basic configuration
    sdk = SdkOperations(show_code=False)
    config = sdk.create_configuration(endpoint=endpoint, use_console=False)
    sdk.apply_signal_specific_endpoints(config, endpoints)
    
    print_success("Configuration created successfully")
    print_info(f"Default endpoint: {endpoint}")
    
    return config


def example_02_console_exporter():
    """Example 2: Enable console exporter for debugging"""
    print_example_section("Example 2: Console Exporter")
    print_info("Enable console output to see telemetry data in the terminal")
    
    _, endpoint, _, endpoints = load_environment()
    
    # Create configuration and enable console exporter
    sdk = SdkOperations(show_code=False)
    config = sdk.create_configuration(endpoint=endpoint, use_console=True)
    sdk.apply_signal_specific_endpoints(config, endpoints)
    
    print_success("Console exporter enabled")
    print_info("Telemetry data will be printed to console")
    
    return config


def example_03_signal_specific_endpoints():
    """Example 3: Set different endpoints for different signals"""
    print_example_section("Example 3: Signal-Specific Endpoints")
    print_info("Configure separate endpoints for metrics, logs, and traces")
    
    _, default_endpoint, _, _ = load_environment()
    
    # Create configuration with default endpoint
    sdk = SdkOperations(show_code=False)
    config = sdk.create_configuration(endpoint=default_endpoint, use_console=False)
    
    # Set signal-specific endpoints (using same endpoint for demo)
    sdk.set_signal_endpoints(
        config,
        metrics_endpoint=default_endpoint,
        logging_endpoint=default_endpoint,
        tracing_endpoint=default_endpoint
    )
    
    print_success("Signal-specific endpoints configured")
    print_info(f"Metrics endpoint: {default_endpoint}")
    print_info(f"Logging endpoint: {default_endpoint}")
    print_info(f"Tracing endpoint: {default_endpoint}")
    
    return config


def example_04_export_intervals():
    """Example 4: Configure export intervals"""
    print_example_section("Example 4: Export Intervals")
    print_info("Set how often telemetry data is sent to the collector")
    
    _, endpoint, _, endpoints = load_environment()
    
    # Create configuration
    sdk = SdkOperations(show_code=False)
    config = sdk.create_configuration(
        endpoint=endpoint,
        use_console=False,
        metrics_interval_ms=ExportInterval.METRICS_30S.value,
        tracing_interval_ms=ExportInterval.TRACING_15S.value
    )
    sdk.apply_signal_specific_endpoints(config, endpoints)
    
    print_success("Export intervals configured")
    print_info("Metrics export interval: 30 seconds")
    print_info("Tracing export interval: 15 seconds")
    
    return config


def example_05_logging_level():
    """Example 5: Set logging level"""
    print_example_section("Example 5: Logging Level")
    print_info("Configure which log levels are sent to the collector")
    
    _, endpoint, _, endpoints = load_environment()
    
    # Create configuration
    sdk = SdkOperations(show_code=False)
    config = sdk.create_configuration(
        endpoint=endpoint,
        use_console=False,
        logging_level=LoggingLevel.INFO.value
    )
    sdk.apply_signal_specific_endpoints(config, endpoints)
    
    print_success("Logging level configured")
    print_info("Logging level: info (info, warning, error will be sent)")
    
    return config


def example_06_session_entropy():
    """Example 6: Set session entropy for unique session IDs"""
    print_example_section("Example 6: Session Entropy")
    print_info("Set custom entropy value for generating unique session IDs")
    
    _, endpoint, _, endpoints = load_environment()
    
    # Create configuration
    sdk = SdkOperations(show_code=False)
    import time
    session_entropy = int(time.time() * 1000)
    config = sdk.create_configuration(
        endpoint=endpoint,
        use_console=False,
        session_entropy=session_entropy
    )
    sdk.apply_signal_specific_endpoints(config, endpoints)
    
    print_success("Session entropy configured")
    print_info(f"Session entropy: {session_entropy}")
    
    return config


def example_07_skip_internet_check():
    """Example 7: Skip internet connectivity check"""
    print_example_section("Example 7: Skip Internet Check")
    print_info("Disable internet connectivity check for offline environments")
    
    _, endpoint, _, endpoints = load_environment()
    
    # Create configuration
    sdk = SdkOperations(show_code=False)
    config = sdk.create_configuration(
        endpoint=endpoint,
        use_console=False,
        skip_internet_check=True
    )
    sdk.apply_signal_specific_endpoints(config, endpoints)
    
    print_success("Internet check disabled")
    print_info("SDK will not check for internet connectivity")
    
    return config


def example_08_cumulative_metrics():
    """Example 8: Enable cumulative metrics aggregation"""
    print_example_section("Example 8: Cumulative Metrics")
    print_info("Enable cumulative aggregation for metrics (vs delta)")
    
    _, endpoint, _, endpoints = load_environment()
    
    # Create configuration
    sdk = SdkOperations(show_code=False)
    config = sdk.create_configuration(
        endpoint=endpoint,
        use_console=False,
        use_cumulative_metrics=True
    )
    sdk.apply_signal_specific_endpoints(config, endpoints)
    
    print_success("Cumulative metrics enabled")
    print_info("Metrics will use cumulative aggregation")
    
    return config


def example_09_complete_configuration():
    """Example 9: Complete configuration with all options"""
    print_example_section("Example 9: Complete Configuration")
    print_info("Combine multiple configuration options")
    
    _, endpoint, _, endpoints = load_environment()
    
    # Create comprehensive configuration
    sdk = SdkOperations(show_code=False)
    import time
    config = sdk.create_configuration(
        endpoint=endpoint,
        use_console=True,
        metrics_interval_ms=ExportInterval.METRICS_60S.value,
        tracing_interval_ms=ExportInterval.TRACING_30S.value,
        logging_level=LoggingLevel.WARNING.value,
        session_entropy=int(time.time() * 1000)
    )
    sdk.apply_signal_specific_endpoints(config, endpoints)
    
    print_success("Complete configuration created")
    print_info("[OK] Console exporter enabled")
    print_info("[OK] Export intervals configured")
    print_info("[OK] Logging level set to 'warning'")
    print_info("[OK] Session entropy configured")
    
    return config


def run_all_examples():
    """Run all configuration examples"""
    print_example_header(
        "Configuration Examples",
        "Demonstrating Configuration class and its methods"
    )
    
    # Validate environment
    validate_environment()
    
    # Run examples
    example_01_basic_configuration()
    example_02_console_exporter()
    example_03_signal_specific_endpoints()
    example_04_export_intervals()
    example_05_logging_level()
    example_06_session_entropy()
    example_07_skip_internet_check()
    example_08_cumulative_metrics()
    example_09_complete_configuration()
    
    print("\n" + "=" * 70)
    print_success("All configuration examples completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_all_examples()
