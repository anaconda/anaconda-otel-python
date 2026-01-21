#!/usr/bin/env python3
"""
Example 13: Logging with Explicit Flush

Demonstrates explicit flush functionality for logging to ensure telemetry data
is sent before the application exits. Similar to Example 7 but focused on logging.

WHEN TO USE THIS APPROACH:
- Short-lived processes or scripts that need guaranteed log delivery
- Lambda functions or serverless applications
- Testing and validation scenarios where you need to confirm logs were sent
- Applications that need to ensure logs are exported before shutdown
- Batch jobs or CLI tools with critical logging

USE CASES:
- Short-lived CLI tools or batch jobs
- Lambda functions or serverless applications
- Testing and validation scenarios
- Applications where you need guaranteed delivery before shutdown
- Scripts that need to confirm log export completed

NOTE: For Python, the OpenTelemetry SDK automatically handles flushing when
the process ends. Explicit flush is typically not necessary but is supported
for cases where you need immediate export or want to ensure data is sent
before continuing execution.
"""

import logging
from anaconda.opentelemetry import (
    Configuration, 
    ResourceAttributes, 
    initialize_telemetry
)
from anaconda.opentelemetry.signals import get_telemetry_logger_handler
from utils import (
    EndpointType,
    load_environment,
    print_header,
    print_footer,
    print_info,
    print_code,
    print_section,
    print_environment_config,
    flush_logs,
    apply_signal_specific_endpoints
)
from test_data import (
    ServiceVersion,
    LogMessage,
    LogAttributes,
    LoggerName,
    ServiceNameLogging
)

# Test data constants
SERVICE_NAME = ServiceNameLogging.LOGGING_FLUSH.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
LOGGER_NAME = LoggerName.APP_LOGGER.value


def main():
    print_header("Example 13: Logging with Explicit Flush", 
                 "Verify flush functionality for logging doesn't break telemetry flow")
    
    # Load environment
    _, endpoint, use_console, endpoints = load_environment()
    print_environment_config(endpoint, use_console)
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    apply_signal_specific_endpoints(config, endpoints)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    # Create attributes
    attrs = ResourceAttributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Initialize with logging enabled
    print_section("1. Initialize Telemetry with Logging")
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['logging']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['logging'])")
    print_info("✓ Telemetry initialized with logging enabled")
    
    # Get the telemetry logger handler
    print_section("2. Configure Logger")
    handler = get_telemetry_logger_handler()
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    print_code(f'logger = logging.getLogger("{LOGGER_NAME}")')
    print_code("logger.addHandler(get_telemetry_logger_handler())")
    print_info("✓ Logger configured")
    
    # Send multiple log messages
    print_section("3. Send Log Messages")
    
    print_info("\n  Sending INFO log:")
    logger.info(LogMessage.USER_LOGIN.value, extra=LogAttributes.USER_BASIC.value)
    print_code(f'logger.info("{LogMessage.USER_LOGIN.value}", extra=USER_BASIC)')
    
    print_info("\n  Sending WARNING log:")
    logger.warning(LogMessage.SLOW_QUERY.value, extra=LogAttributes.DB_SLOW_QUERY.value)
    print_code(f'logger.warning("{LogMessage.SLOW_QUERY.value}", extra=DB_SLOW_QUERY)')
    
    print_info("\n  Sending ERROR log:")
    logger.error(LogMessage.CONNECTION_FAILED.value, extra=LogAttributes.ERROR_CONTEXT.value)
    print_code(f'logger.error("{LogMessage.CONNECTION_FAILED.value}", extra=ERROR_CONTEXT)')
    
    print_info("\n✓ All log messages sent")
    
    # Explicit flush
    print_section("4. Explicit Flush")
    print_info("Flushing logging telemetry data...")
    print_code("flush_logs()")
    flush_logs()
    print_info("✓ Flush completed successfully")
    print_info("\nNote: Python SDK automatically flushes on process exit.")
    print_info("Explicit flush is useful for:")
    print_info("  • Short-lived processes (Lambda, CLI tools)")
    print_info("  • Testing and validation")
    print_info("  • Ensuring logs are sent before continuing")
    
    # SDK Commands Summary
    print_section("SDK Commands Summary")
    print_info("Commands used in this example:")
    print_code("1. initialize_telemetry(config, attrs, signal_types=['logging'])")
    print_code("2. get_telemetry_logger_handler()")
    print_code("3. logger.info/warning/error(message, extra={...})")
    print_code("4. flush_logs()  # Explicitly flush logging data")
    
    # Backend validation
    print_section("Backend Validation")
    print_info("To validate in backend:")
    print_info(f"  • Service Name: {SERVICE_NAME}")
    print_info(f"  • Service Version: {SERVICE_VERSION}")
    print_info("  • Expected 3 log records:")
    print_info(f"    - INFO: {LogMessage.USER_LOGIN.value}")
    print_info(f"    - WARNING: {LogMessage.SLOW_QUERY.value}")
    print_info(f"    - ERROR: {LogMessage.CONNECTION_FAILED.value}")
    print_info("  • All logs should have attributes and resource attributes")
    print_info("  • Logs should appear in backend within export interval")
    
    print_footer("✓ Example 13 completed successfully!")


if __name__ == "__main__":
    main()
