# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Configuration Examples

This module demonstrates how to create and configure Configuration objects
for the Anaconda OpenTelemetry SDK.
"""

from anaconda.opentelemetry import Configuration
from utils import (
    load_environment,
    print_example_header,
    print_example_section,
    print_success,
    print_info,
    validate_environment
)
from test_data import ExportInterval, LoggingLevel


def example_01_basic_configuration():
    """Example 1: Create basic configuration with default endpoint"""
    print_example_section("Example 1: Basic Configuration")
    print_info("Create a Configuration with a default endpoint")
    
    # Get endpoint from environment
    _, endpoint, _ = load_environment()
    
    # Create basic configuration
    config = Configuration(default_endpoint=endpoint)
    
    print_success("Configuration created successfully")
    print_info(f"Default endpoint: {endpoint}")
    
    return config


def example_02_console_exporter():
    """Example 2: Enable console exporter for debugging"""
    print_example_section("Example 2: Console Exporter")
    print_info("Enable console output to see telemetry data in the terminal")
    
    _, endpoint, _ = load_environment()
    
    # Create configuration and enable console exporter
    config = Configuration(default_endpoint=endpoint)
    config.set_console_exporter(use_console=True)
    
    print_success("Console exporter enabled")
    print_info("Telemetry data will be printed to console")
    
    return config


def example_03_signal_specific_endpoints():
    """Example 3: Set different endpoints for different signals"""
    print_example_section("Example 3: Signal-Specific Endpoints")
    print_info("Configure separate endpoints for metrics, logs, and traces")
    
    _, default_endpoint, _ = load_environment()
    
    # Create configuration with default endpoint
    config = Configuration(default_endpoint=default_endpoint)
    
    # Set signal-specific endpoints (using same endpoint for demo)
    config.set_metrics_endpoint(default_endpoint)
    config.set_logging_endpoint(default_endpoint)
    config.set_tracing_endpoint(default_endpoint)
    
    print_success("Signal-specific endpoints configured")
    print_info(f"Metrics endpoint: {default_endpoint}")
    print_info(f"Logging endpoint: {default_endpoint}")
    print_info(f"Tracing endpoint: {default_endpoint}")
    
    return config


def example_04_export_intervals():
    """Example 4: Configure export intervals"""
    print_example_section("Example 4: Export Intervals")
    print_info("Set how often telemetry data is sent to the collector")
    
    _, endpoint, _ = load_environment()
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    
    # Set export intervals (in milliseconds)
    config.set_metrics_export_interval_ms(ExportInterval.METRICS_30S.value)  # 30 seconds
    config.set_tracing_export_interval_ms(ExportInterval.TRACING_15S.value)  # 15 seconds
    
    print_success("Export intervals configured")
    print_info("Metrics export interval: 30 seconds")
    print_info("Tracing export interval: 15 seconds")
    
    return config


def example_05_logging_level():
    """Example 5: Set logging level"""
    print_example_section("Example 5: Logging Level")
    print_info("Configure which log levels are sent to the collector")
    
    _, endpoint, _ = load_environment()
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    
    # Set logging level (only logs at this level or higher will be sent)
    config.set_logging_level(LoggingLevel.INFO.value)
    
    print_success("Logging level configured")
    print_info("Logging level: info (info, warning, error will be sent)")
    
    return config


def example_06_session_entropy():
    """Example 6: Set session entropy for unique session IDs"""
    print_example_section("Example 6: Session Entropy")
    print_info("Set custom entropy value for generating unique session IDs")
    
    _, endpoint, _ = load_environment()
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    
    # Set session entropy (any value that makes sessions unique)
    import time
    session_entropy = int(time.time() * 1000)
    config.set_tracing_session_entropy(session_entropy)
    
    print_success("Session entropy configured")
    print_info(f"Session entropy: {session_entropy}")
    
    return config


def example_07_skip_internet_check():
    """Example 7: Skip internet connectivity check"""
    print_example_section("Example 7: Skip Internet Check")
    print_info("Disable internet connectivity check for offline environments")
    
    _, endpoint, _ = load_environment()
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    
    # Skip internet check (useful for testing or offline environments)
    config.set_skip_internet_check(True)
    
    print_success("Internet check disabled")
    print_info("SDK will not check for internet connectivity")
    
    return config


def example_08_cumulative_metrics():
    """Example 8: Enable cumulative metrics aggregation"""
    print_example_section("Example 8: Cumulative Metrics")
    print_info("Enable cumulative aggregation for metrics (vs delta)")
    
    _, endpoint, _ = load_environment()
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    
    # Enable cumulative metrics
    config.set_use_cumulative_metrics(True)
    
    print_success("Cumulative metrics enabled")
    print_info("Metrics will use cumulative aggregation")
    
    return config


def example_09_complete_configuration():
    """Example 9: Complete configuration with all options"""
    print_example_section("Example 9: Complete Configuration")
    print_info("Combine multiple configuration options")
    
    _, endpoint, _ = load_environment()
    
    # Create comprehensive configuration
    config = Configuration(default_endpoint=endpoint)
    
    # Enable console for debugging
    config.set_console_exporter(use_console=True)
    
    # Set export intervals
    config.set_metrics_export_interval_ms(ExportInterval.METRICS_60S.value)  # 1 minute
    config.set_tracing_export_interval_ms(ExportInterval.TRACING_30S.value)  # 30 seconds
    
    # Set logging level
    config.set_logging_level(LoggingLevel.WARNING.value)
    
    # Set session entropy
    import time
    config.set_tracing_session_entropy(int(time.time() * 1000))
    
    print_success("Complete configuration created")
    print_info("✓ Console exporter enabled")
    print_info("✓ Export intervals configured")
    print_info("✓ Logging level set to 'warning'")
    print_info("✓ Session entropy configured")
    
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
