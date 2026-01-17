# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Print Utilities for E2E QA Examples

This module provides standardized print utilities for consistent output
formatting across all E2E QA examples.
"""


def print_header(title: str, description: str = ""):
    """
    Print a formatted header with title and optional description.
    
    Args:
        title: Main title text
        description: Optional description text
    """
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)
    if description:
        print(f"  {description}")
        print("-" * 70)


def print_footer(message: str):
    """
    Print a formatted footer message.
    
    Args:
        message: Footer message text
    """
    print("\n" + "=" * 70)
    print(f"  {message}")
    print("=" * 70 + "\n")


def print_section(section_name: str):
    """
    Print a formatted section header.
    
    Args:
        section_name: Name of the section
    """
    print(f"\n--- {section_name} ---")


def print_success(message: str):
    """
    Print a success message with checkmark.
    
    Args:
        message: Success message text
    """
    print(f"✓ {message}")


def print_info(message: str, indent: int = 2):
    """
    Print an info message with optional indentation.
    
    Args:
        message: Info message text
        indent: Number of spaces to indent (default: 2)
    """
    print(" " * indent + message)


def print_code(code: str):
    """
    Print a code snippet to show what SDK method is being called.
    
    Args:
        code: Code snippet text
    """
    print(f"  📝 {code}")


def print_environment_config(endpoint: str, use_console: bool, otel_env: str = None):
    """
    Print environment configuration details.
    
    Args:
        endpoint: OTEL endpoint URL
        use_console: Whether console exporter is enabled
        otel_env: Optional OTEL environment name
    """
    if otel_env:
        print_info(f"OTEL Environment: {otel_env}")
    print_info(f"Endpoint: {endpoint}")
    print_info(f"Console Exporter: {use_console}")


def print_resource_attributes(attrs):
    """
    Print resource attributes in a standardized format.
    
    Args:
        attrs: ResourceAttributes object
    """
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


def print_metric_info(metric_name: str, metric_value: any, metric_attrs: dict = None):
    """
    Print metric information.
    
    Args:
        metric_name: Name of the metric
        metric_value: Value of the metric
        metric_attrs: Optional metric-level attributes
    """
    print("\n  📊 Sending Metric:")
    if metric_attrs:
        print_code(f'increment_counter("{metric_name}", by={metric_value}, attributes={metric_attrs})')
    else:
        print_code(f'increment_counter("{metric_name}", by={metric_value})')


def print_backend_validation(service_name: str, metric_name: str, metric_value: any, 
                             attrs, metric_attrs: dict = None):
    """
    Print backend validation checklist.
    
    Args:
        service_name: Service name
        metric_name: Name of the metric
        metric_value: Value of the metric
        attrs: ResourceAttributes object
        metric_attrs: Optional metric-level attributes
    """
    print("\n  ✅ BACKEND VALIDATION CHECKLIST:")
    print("     Query backend for this service:")
    print(f"       WHERE service.name = '{service_name}'")
    print(f"       AND timestamp >= NOW() - INTERVAL '10 minutes'")
    print("\n     Expected in backend:")
    print(f"       • Metric Name: {metric_name}")
    print(f"       • Metric Value: {metric_value}")
    
    if metric_attrs:
        print(f"       • Metric Attributes: {metric_attrs}")
    
    print(f"       • service.name: {service_name}")
    print(f"       • service.version: {attrs.service_version}")
    
    # Print additional attributes based on what's set
    if hasattr(attrs, 'platform') and attrs.platform:
        print(f"       • platform: {attrs.platform}")
    if hasattr(attrs, 'environment') and attrs.environment:
        print(f"       • environment: {attrs.environment}")
    
    print(f"       • os.type: {attrs.os_type}")
    print(f"       • python.version: {attrs.python_version}")
    print(f"       • client.sdk.version: {attrs.client_sdk_version}")
    print(f"       • schema.version: {attrs.schema_version}")
    
    if attrs.parameters:
        print(f"       • parameters: {attrs.parameters}")


def print_flush_status(success: bool = True, error: Exception = None):
    """
    Print telemetry flush status.
    
    Args:
        success: Whether flush was successful
        error: Optional exception if flush failed
    """
    print("\n  Flushing telemetry data...")
    if success:
        print("  ✓ Telemetry flushed to backend")
    else:
        print(f"  ⚠️  Warning: Error during flush: {error}")


def print_initialization_status(signals: list, config_details: dict = None):
    """
    Print telemetry initialization status.
    
    Args:
        signals: List of enabled signals
        config_details: Optional dict with configuration details
    """
    print(f"  ✓ Telemetry initialized")
    print(f"  Enabled: {', '.join(signals)}")
    
    if config_details:
        print("  Configuration:")
        for key, value in config_details.items():
            print(f"    ✓ {key}: {value}")


def print_validation_info(metric_name: str, value: any, attributes: dict = None, 
                         service_name: str = None, resource_attrs: dict = None, 
                         session_id: str = None):
    """
    Print information needed for backend validation (detailed format).
    
    Args:
        metric_name: Name of the metric
        value: Value of the metric
        attributes: Optional metric attributes
        service_name: Service name from ResourceAttributes
        resource_attrs: Additional resource attributes to validate
        session_id: Session ID for backend correlation
    """
    print(f"\n  ⚠️  TODO - VALIDATE BACKEND DATA:")
    
    # Session ID section
    if session_id:
        print(f"     ┌─ Session Information")
        print(f"     │  • Session ID: {session_id}")
        print(f"     │  • Use this to query backend for this specific test run")
        print(f"     │")
        print(f"     ├─ Metric Information")
    else:
        print(f"     ┌─ Session Information")
        print(f"     │  • Session ID: See console JSON output or summary at end")
        print(f"     │  • All metrics in this run share the same session ID")
        print(f"     │")
        print(f"     ├─ Metric Information")
    
    print(f"     │  • Metric Name: {metric_name}")
    print(f"     │  • Expected Value: {value}")
    if attributes:
        print(f"     │  • Metric Attributes: {attributes}")
    
    # Resource Attributes section
    if service_name:
        print(f"     │")
        print(f"     ├─ Resource Attributes")
        print(f"     │  • service.name: {service_name}")
        if resource_attrs:
            for key, val in resource_attrs.items():
                print(f"     │  • {key}: {val}")
    
    # Verification Steps section
    print(f"     │")
    print(f"     └─ Verification Steps")
    print(f"        1. Check metric appears in backend within some delay")
    if session_id:
        print(f"        2. Query backend using session ID above")
        print(f"        3. Verify metric name matches exactly")
        print(f"        4. Verify value is correct")
        if attributes:
            print(f"        5. Verify metric attributes are present")
        if service_name:
            print(f"        6. Verify resource attributes match")
    else:
        print(f"        2. Verify metric name matches exactly")
        print(f"        3. Verify value is correct")
        if attributes:
            print(f"        4. Verify metric attributes are present")
        if service_name:
            print(f"        5. Verify resource attributes match")


def print_example_header(title: str, description: str = ""):
    """
    Alias for print_header for backward compatibility.
    
    Args:
        title: Main title text
        description: Optional description text
    """
    print_header(title, description)


def print_example_section(section_name: str):
    """
    Alias for print_section for backward compatibility.
    
    Args:
        section_name: Name of the section
    """
    print_section(section_name)
