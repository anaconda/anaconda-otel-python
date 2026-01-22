# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Print Utilities for E2E QA Examples

This module provides standardized print utilities for consistent output
formatting across all E2E QA examples.
"""

import os
import re
import sys
import subprocess
from typing import List, Dict, Tuple


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
    print(f"[OK] {message}")


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
    print(f"  [CODE] {code}")


def log_detailed(message: str):
    """
    Log detailed information if USE_DETAILED_LOG environment variable is enabled.
    
    This function provides optional verbose logging for debugging and development.
    Enable by setting: USE_DETAILED_LOG=true
    
    Args:
        message: Detailed log message text
        
    Example:
        log_detailed("Sending counter: api_requests_total")
        log_detailed(f"  -> Value: {value}, Attributes: {attrs}")
        log_detailed("[OK] Counter queued successfully")
    """
    if os.getenv('USE_DETAILED_LOG', 'false').lower() == 'true':
        print_info(f"[DETAILED] {message}")


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
    print("\n  [ATTRS] Resource Attributes (sent with every metric):")
    print(f"     - service.name: {attrs.service_name}")
    print(f"     - service.version: {attrs.service_version}")
    print(f"     - os.type: {attrs.os_type}")
    print(f"     - os.version: {attrs.os_version}")
    print(f"     - python.version: {attrs.python_version}")
    print(f"     - hostname: {attrs.hostname}")
    print(f"     - platform: {attrs.platform if attrs.platform else '(empty)'}")
    print(f"     - environment: {attrs.environment if attrs.environment else '(empty)'}")
    print(f"     - client.sdk.version: {attrs.client_sdk_version}")
    print(f"     - schema.version: {attrs.schema_version}")
    print(f"     - session.id: (auto-generated, visible with console exporter)")
    if attrs.parameters:
        print(f"     - parameters: {attrs.parameters}")


def print_metric_info(metric_name: str, metric_value: any, metric_attrs: dict = None):
    """
    Print metric information.
    
    Args:
        metric_name: Name of the metric
        metric_value: Value of the metric
        metric_attrs: Optional metric-level attributes
    """
    print("\n  [METRIC] Sending Metric:")
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
    print("\n  [VALIDATE] BACKEND VALIDATION CHECKLIST:")
    print("     Query backend for this service:")
    print(f"       WHERE service.name = '{service_name}'")
    print(f"       AND timestamp >= NOW() - INTERVAL '10 minutes'")
    print("\n     Expected in backend:")
    print(f"       - Metric Name: {metric_name}")
    print(f"       - Metric Value: {metric_value}")
    
    if metric_attrs:
        print(f"       - Metric Attributes: {metric_attrs}")
    
    print(f"       - service.name: {service_name}")
    print(f"       - service.version: {attrs.service_version}")
    
    # Print additional attributes based on what's set
    if hasattr(attrs, 'platform') and attrs.platform:
        print(f"       - platform: {attrs.platform}")
    if hasattr(attrs, 'environment') and attrs.environment:
        print(f"       - environment: {attrs.environment}")
    
    print(f"       - os.type: {attrs.os_type}")
    print(f"       - python.version: {attrs.python_version}")
    print(f"       - client.sdk.version: {attrs.client_sdk_version}")
    print(f"       - schema.version: {attrs.schema_version}")
    
    if attrs.parameters:
        print(f"       - parameters: {attrs.parameters}")


def print_sdk_commands_summary(commands: list):
    """
    Print a concise summary of SDK commands called.
    
    Args:
        commands: List of command strings or tuples (command, description)
    """
    print("\n  [SDK] SDK COMMANDS CALLED:")
    for i, cmd in enumerate(commands, 1):
        if isinstance(cmd, tuple):
            command, description = cmd
            print(f"     {i}. {command}")
            if description:
                print(f"        -> {description}")
        else:
            print(f"     {i}. {cmd}")


def print_flush_status(success: bool = True, error: Exception = None):
    """
    Print telemetry flush status.
    
    Args:
        success: Whether flush was successful
        error: Optional exception if flush failed
    """
    print("\n  Flushing telemetry data...")
    if success:
        print("  [OK] Telemetry flushed to backend")
    else:
        print(f"  [WARN] Warning: Error during flush: {error}")


def print_initialization_status(signals: list, config_details: dict = None):
    """
    Print telemetry initialization status.
    
    Args:
        signals: List of enabled signals
        config_details: Optional dict with configuration details
    """
    print(f"  [OK] Telemetry initialized")
    print(f"  Enabled: {', '.join(signals)}")
    
    if config_details:
        print("  Configuration:")
        for key, value in config_details.items():
            print(f"    [OK] {key}: {value}")


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
    print(f"\n  [TODO] TODO - VALIDATE BACKEND DATA:")
    
    # Session ID section
    if session_id:
        print(f"     +-- Session Information")
        print(f"     |  - Session ID: {session_id}")
        print(f"     |  - Use this to query backend for this specific test run")
        print(f"     |")
        print(f"     +-- Metric Information")
    else:
        print(f"     +-- Session Information")
        print(f"     |  - Session ID: See console JSON output or summary at end")
        print(f"     |  - All metrics in this run share the same session ID")
        print(f"     |")
        print(f"     +-- Metric Information")
    
    print(f"     |  - Metric Name: {metric_name}")
    print(f"     |  - Expected Value: {value}")
    if attributes:
        print(f"     |  - Metric Attributes: {attributes}")
    
    # Resource Attributes section
    if service_name:
        print(f"     |")
        print(f"     +-- Resource Attributes")
        print(f"     |  - service.name: {service_name}")
        if resource_attrs:
            for key, val in resource_attrs.items():
                print(f"     |  - {key}: {val}")
    
    # Verification Steps section
    print(f"     |")
    print(f"     +-- Verification Steps")
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


# ============================================================================
# Error Detection and Reporting Utilities
# ============================================================================


def extract_http_errors(output: str) -> List[str]:
    """
    Extract HTTP error messages from output.
    
    Args:
        output: Command output text
        
    Returns:
        List of error messages found
    """
    errors = []
    
    # Pattern for HTTP error codes
    http_error_patterns = [
        # OpenTelemetry export failures (e.g., "Failed to export logs batch code: 404")
        r'Failed to export.*?code:\s*(\d{3})',
        # Generic HTTP errors
        r'(HTTP\s+)?(\d{3})\s+(Error|Not Found|Forbidden|Unauthorized|Bad Request|Internal Server Error)',
        r'status[_\s]code[:\s]+(\d{3})',
        r'(\d{3})\s+Client Error',
        r'(\d{3})\s+Server Error',
        r'Failed to send.*?(\d{3})',
        # Connection errors
        r'Connection.*?failed',
        r'Connection.*?refused',
        r'Connection.*?reset',
        # Timeout errors - more specific patterns to avoid matching documentation text
        r'TimeoutError:',                      # Python exception
        r'timed out after \d+',                # Actual timeout message
        r'Export.*?timeout',                   # Export timeout
        r'Connection.*?timeout',               # Connection timeout
        r'Request timeout after \d+',          # Request timeout with duration
        # DNS errors
        r'Name or service not known',
        r'nodename nor servname provided',
        r'Temporary failure in name resolution',
    ]
    
    for pattern in http_error_patterns:
        matches = re.finditer(pattern, output, re.IGNORECASE)
        for match in matches:
            # Extract the full line containing the error
            line_start = output.rfind('\n', 0, match.start()) + 1
            line_end = output.find('\n', match.end())
            if line_end == -1:
                line_end = len(output)
            error_line = output[line_start:line_end].strip()
            if error_line and error_line not in errors:
                errors.append(error_line)
    
    return errors


def process_subprocess_output(result_stdout: str, result_stderr: str) -> List[str]:
    """
    Process subprocess output and extract errors.
    
    Args:
        result_stdout: Standard output from subprocess
        result_stderr: Standard error from subprocess
        
    Returns:
        List of extracted errors
    """
    errors = []
    
    # Print stdout
    if result_stdout:
        print(result_stdout, end='')
        errors.extend(extract_http_errors(result_stdout))
    
    # Print stderr and extract errors
    if result_stderr:
        print(result_stderr, end='', file=sys.stderr)
        errors.extend(extract_http_errors(result_stderr))
    
    return errors


def run_example_subprocess(script_path: str, python_executable: str = None) -> Tuple[bool, List[str]]:
    """
    Run an example script as a subprocess with error tracking.
    
    This is a generalized function for running example scripts that:
    - Executes the script in a separate process
    - Captures and displays output in real-time
    - Extracts and tracks HTTP/connection errors
    - Returns success status and detected errors
    
    Args:
        script_path: Path to the example script to run
        python_executable: Python executable to use (defaults to sys.executable)
        
    Returns:
        Tuple of (success: bool, errors: List[str])
        
    Example:
        success, errors = run_example_subprocess("examples/01_test.py")
        if not success:
            print(f"Script failed with {len(errors)} errors")
    """
    if python_executable is None:
        python_executable = sys.executable
    
    errors = []
    try:
        result = subprocess.run(
            [python_executable, script_path],
            check=True,
            capture_output=True,
            text=True
        )
        # Process output and extract errors
        errors.extend(process_subprocess_output(result.stdout, result.stderr))
        return True, errors
    except subprocess.CalledProcessError as e:
        print(f"\n[FAIL] Example failed: {script_path}")
        print(f"   Exit code: {e.returncode}")
        # Process output and extract errors
        errors.extend(process_subprocess_output(e.stdout, e.stderr))
        return False, errors
    except Exception as e:
        print(f"\n[FAIL] Error running example: {script_path}")
        print(f"   Error: {e}")
        errors.append(f"Exception: {str(e)}")
        return False, errors


def print_examples_summary(results: Dict[str, Tuple[bool, List[str]]], 
                          title: str = "Examples",
                          emoji: str = "[RUN]") -> Tuple[int, int, Dict[str, List[str]]]:
    """
    Print summary of examples with error indicators.
    
    Args:
        results: Dict mapping example names to (success, errors) tuples
        title: Title for the summary section
        emoji: Emoji to use in the title
        
    Returns:
        Tuple of (success_count, total_count, error_by_example)
    """
    print(f"\n{emoji} {title}:")
    success_count = 0
    error_by_example = {}
    
    for script, (success, errors) in results.items():
        status = "[OK]" if success else "[FAIL]"
        error_indicator = " [WARN]" if errors else ""
        print(f"   {status} {script}{error_indicator}")
        if success:
            success_count += 1
        if errors:
            error_by_example[script] = errors
    
    total_count = len(results)
    print(f"   Total: {success_count}/{total_count} successful")
    
    return success_count, total_count, error_by_example


def print_error_highlights(all_errors: List[str], error_by_example: Dict[str, List[str]]):
    """
    Print detailed error highlights section with categorization.
    
    Args:
        all_errors: List of all errors detected
        error_by_example: Dict mapping example names to their errors
    """
    if not all_errors:
        return
    
    print("\n" + "=" * 70)
    print("[WARN] ERRORS DETECTED")
    print("=" * 70)
    
    # Categorize errors
    http_404_errors = [e for e in all_errors if '404' in e]
    http_other_errors = [e for e in all_errors if re.search(r'\b(4\d{2}|5\d{2})\b', e) and '404' not in e]
    connection_errors = [e for e in all_errors if 'connection' in e.lower() or 'timeout' in e.lower()]
    other_errors = [e for e in all_errors if e not in http_404_errors + http_other_errors + connection_errors]
    
    # Print categorized errors
    if http_404_errors:
        print("\n[ERROR] HTTP 404 Errors (Not Found):")
        unique_404s = list(dict.fromkeys(http_404_errors))  # Remove duplicates while preserving order
        for error in unique_404s[:5]:  # Show first 5
            print(f"   - {error}")
        if len(unique_404s) > 5:
            print(f"   ... and {len(unique_404s) - 5} more")
    
    if http_other_errors:
        print("\n[ERROR] Other HTTP Errors:")
        unique_others = list(dict.fromkeys(http_other_errors))
        for error in unique_others[:5]:
            print(f"   - {error}")
        if len(unique_others) > 5:
            print(f"   ... and {len(unique_others) - 5} more")
    
    if connection_errors:
        print("\n[ERROR] Connection/Timeout Errors:")
        unique_conn = list(dict.fromkeys(connection_errors))
        for error in unique_conn[:5]:
            print(f"   - {error}")
        if len(unique_conn) > 5:
            print(f"   ... and {len(unique_conn) - 5} more")
    
    if other_errors:
        print("\n[ERROR] Other Errors:")
        unique_other = list(dict.fromkeys(other_errors))
        for error in unique_other[:5]:
            print(f"   - {error}")
        if len(unique_other) > 5:
            print(f"   ... and {len(unique_other) - 5} more")
    
    # Show which examples had errors
    print("\n[INFO] Examples with Errors:")
    for example, errors in error_by_example.items():
        print(f"   - {example} ({len(errors)} error(s))")
    
    # Troubleshooting guidance
    print("\n[TIP] Troubleshooting:")
    if http_404_errors:
        print("   - 404 errors may indicate incorrect endpoint configuration")
        print("   - Verify OTEL_ENDPOINT in .env file")
        print("   - Check that the backend service is running and accessible")
    if connection_errors:
        # Check for DNS-specific errors
        dns_errors = [e for e in connection_errors if 'failed to resolve' in e.lower() or 'nameresolutionerror' in e.lower()]
        if dns_errors:
            print("   - DNS resolution errors detected - check endpoint URL for typos")
            print("   - Verify OTEL_ENDPOINT in .env file (check spelling)")
            print("   - Ensure the hostname is correct and accessible")
        else:
            print("   - Connection errors may indicate network issues")
            print("   - Verify internet connectivity")
            print("   - Check firewall settings")
    
    print("=" * 70)


def print_initialization_header(env: str, endpoint: str, use_console: bool):
    """
    Print header for initialization examples runner.
    
    Args:
        env: Environment name
        endpoint: OTEL endpoint URL
        use_console: Whether console exporter is enabled
    """
    print("\n" + "=" * 70)
    print("  Running Initialization Examples")
    print("=" * 70)
    print("  Each example runs in a separate process for proper initialization")
    print("-" * 70)
    
    print(f"  Environment: {env}")
    print(f"  Endpoint: {endpoint}")
    print(f"  Console Exporter: {use_console}")
    
    if use_console:
        print("\n  [WARN] WARNING: Console exporter is enabled!")
        print("     Data will be printed to console but NOT sent to backend.")
        print("     Set OTEL_CONSOLE_EXPORTER=false for backend validation.")
    else:
        print("\n  [OK] Console exporter is disabled - data will be sent to backend")
    
    print("=" * 70 + "\n")


def print_initialization_summary(
    results: Dict[str, Tuple[bool, List[str]]], 
    config_results: Dict[str, Tuple[bool, List[str]]] = None,
    use_console: bool = False
):
    """
    Print comprehensive summary for initialization examples.
    
    Args:
        results: Dict mapping initialization example names to (success, errors) tuples
        config_results: Optional dict for configuration examples
        use_console: Whether console exporter is enabled
    """
    print("\n" + "=" * 70)
    print("[SUMMARY]")
    print("=" * 70)
    
    # Collect all errors
    all_errors = []
    all_error_by_example = {}
    
    # Console exporter warning
    if use_console:
        print("\n[WARN] CRITICAL WARNING:")
        print("   OTEL_CONSOLE_EXPORTER=true in .env")
        print("   Data is ONLY printed to console, NOT sent to backend!")
        print("   To validate in backend: Set OTEL_CONSOLE_EXPORTER=false")
        print("=" * 70)
    
    # Configuration examples summary
    config_success = 0
    if config_results:
        config_success, _, error_by_example = print_examples_summary(
            config_results, 
            title="Configuration Examples",
            emoji="[CONFIG]"
        )
        all_error_by_example.update(error_by_example)
        for errors in error_by_example.values():
            all_errors.extend(errors)
    
    # Initialization examples summary
    success_count, total_count, error_by_example = print_examples_summary(
        results,
        title="Initialization Examples",
        emoji="[INIT]"
    )
    all_error_by_example.update(error_by_example)
    for errors in error_by_example.values():
        all_errors.extend(errors)
    
    # Overall summary
    total_all = total_count + (len(config_results) if config_results else 0)
    success_all = success_count + config_success
    
    # Print error highlights
    print_error_highlights(all_errors, all_error_by_example)
    
    # Final status
    if success_all == total_all:
        print("\n[SUCCESS] All examples completed successfully!")
        
        if all_errors:
            print("   [WARN] However, some HTTP errors were detected during execution")
            print("   [WARN] See error details above")
        
        if not use_console:
            print("\n[TIP] To validate in backend:")
            print("   1. Wait 1-5 minutes for backend processing")
            print("   2. Query by service names:")
            print("      - example-01-all-signals")
            print("      - example-02-metrics-only")
            print("      - example-03-default")
            print("      - example-04-selective")
            print("      - example-05-complete")
            print("      - example-06-env-based")
            print("      - example-07-flush-test")
            print("   3. Each service should have 1 metric with value=1")
    else:
        print("\n[FAIL] Some examples failed - check output above for errors")
    
    print("=" * 70 + "\n")


def print_logging_header():
    """Print header for logging examples runner."""
    print("\n" + "=" * 80)
    print("  Running Logging Examples")
    print("=" * 80)
    print("This will run all logging examples in sequence.")
    print("Each example demonstrates different logging capabilities.")


def print_logging_summary(results: Dict[str, Tuple[bool, List[str]]]):
    """
    Print comprehensive summary for logging examples.
    
    Args:
        results: Dict mapping example names to (success, errors) tuples
    """
    print("\n" + "=" * 80)
    print("[SUMMARY]")
    print("=" * 80)
    
    # Use utility function for consistent summary
    success_count, total_count, error_by_example = print_examples_summary(
        results,
        title="Logging Examples",
        emoji="[LOG]"
    )
    
    # Collect all errors
    all_errors = []
    for errors in error_by_example.values():
        all_errors.extend(errors)
    
    # Print error highlights
    print_error_highlights(all_errors, error_by_example)
    
    # Final status
    if success_count == total_count:
        print("\n[SUCCESS] All logging examples completed successfully!")
        
        if all_errors:
            print("   [WARN] However, some HTTP errors were detected during execution")
            print("   [WARN] See error details above")
    else:
        print("\n[FAIL] Some examples failed - check output above for errors")
    
    # Backend validation info
    print("\n[TIP] To validate in backend:")
    print("   Expected services:")
    print("     1. example-08-logging-basic")
    print("     2. example-09-logging-levels")
    print("     3. example-10-logging-structured")
    print("     4. example-11-logging-multiple")
    print("     5. example-12-logging-integration")
    print("     6. example-13-logging-flush")
    print("\n   Each service should have log records with:")
    print("     - Proper severity levels")
    print("     - Resource attributes")
    print("     - Structured attributes (where applicable)")
    print("     - Logger names (where applicable)")
    
    print("=" * 80 + "\n")


def print_metrics_header():
    """Print header for metrics examples runner."""
    print("\n" + "=" * 80)
    print("  Running Metrics Examples")
    print("=" * 80)
    print("This will run all metrics examples in sequence.")
    print("Each example demonstrates different metrics capabilities.")


def print_metrics_summary(results: Dict[str, Tuple[bool, List[str]]]):
    """
    Print comprehensive summary for metrics examples.
    
    Args:
        results: Dict mapping example names to (success, errors) tuples
    """
    print("\n" + "=" * 80)
    print("[SUMMARY]")
    print("=" * 80)
    
    # Use utility function for consistent summary
    success_count, total_count, error_by_example = print_examples_summary(
        results,
        title="Metrics Examples",
        emoji="[METRIC]"
    )
    
    # Collect all errors
    all_errors = []
    for errors in error_by_example.values():
        all_errors.extend(errors)
    
    # Print error highlights
    print_error_highlights(all_errors, error_by_example)
    
    # Final status
    if success_count == total_count:
        print("\n[SUCCESS] All metrics examples completed successfully!")
        
        if all_errors:
            print("   [WARN] However, some HTTP errors were detected during execution")
            print("   [WARN] See error details above")
    else:
        print("\n[FAIL] Some examples failed - check output above for errors")
    
    # Backend validation info
    print("\n[TIP] To validate in backend:")
    print("   Expected services:")
    print("     1. example-14-metrics-counters")
    print("     2. example-15-metrics-histogram")
    print("     3. example-16-metrics-updown")
    print("     4. example-17-metrics-attributes")
    print("     5. example-18-metrics-patterns")
    print("     6. example-19-metrics-flush")
    print("\n   Each service should have metrics with:")
    print("     - Proper metric types (counter, histogram, up/down counter)")
    print("     - Resource attributes")
    print("     - Metric-level attributes (where applicable)")
    print("     - Correct values and aggregations")
    
    print("=" * 80 + "\n")
