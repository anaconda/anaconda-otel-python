#!/usr/bin/env python3
"""
Example 8: Basic Logging

Demonstrates basic logging functionality including getting the telemetry logger
handler and sending log messages at different levels.

WHEN TO USE THIS APPROACH:
- You need to send structured logs to your telemetry backend
- You want to integrate OpenTelemetry logging into your application
- You need to track application events and errors with context
- You want logs to be correlated with metrics and traces

USE CASES:
- Application event logging (user actions, system events)
- Error tracking and debugging
- Audit logging for compliance
- Performance monitoring through log analysis
- Structured logging for better searchability

KEY CONCEPTS:
- get_telemetry_logger_handler(): Returns a logging handler for OpenTelemetry
- The handler must be added to your Python logger
- Logs are exported to the configured backend (or console)
- Supports all standard Python logging levels
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
    LoggerName,
    ServiceNameLogging
)

# Test data constants
SERVICE_NAME = ServiceNameLogging.LOGGING_BASIC.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
LOGGER_NAME = LoggerName.APP_LOGGER.value


def main():
    print_header("Example 8: Basic Logging", 
                 "Get telemetry logger handler and send basic log messages")
    
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
        signal_types=['logging']  # Only logging for this example
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['logging'])")
    print_info("✓ Telemetry initialized with logging enabled")
    
    # Get the telemetry logger handler
    print_section("2. Get Telemetry Logger Handler")
    handler = get_telemetry_logger_handler()
    print_code("handler = get_telemetry_logger_handler()")
    print_info("✓ Retrieved telemetry logger handler")
    
    # Create a logger and add the handler
    print_section("3. Create Logger and Add Handler")
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    print_code(f'logger = logging.getLogger("{LOGGER_NAME}")')
    print_code("logger.setLevel(logging.DEBUG)")
    print_code("logger.addHandler(handler)")
    print_info(f"✓ Logger '{LOGGER_NAME}' configured with telemetry handler")
    
    # Send log messages at different levels
    print_section("4. Send Log Messages at Different Levels")
    
    print_info("\n  Sending INFO log:")
    logger.info(LogMessage.BASIC_INFO.value)
    print_code(f'logger.info("{LogMessage.BASIC_INFO.value}")')
    
    print_info("\n  Sending INFO log (user logout):")
    logger.info(LogMessage.USER_LOGOUT.value)
    print_code(f'logger.info("{LogMessage.USER_LOGOUT.value}")')
    
    print_info("\n  Sending WARNING log:")
    logger.warning(LogMessage.BASIC_WARNING.value)
    print_code(f'logger.warning("{LogMessage.BASIC_WARNING.value}")')
    
    print_info("\n  Sending ERROR log:")
    logger.error(LogMessage.BASIC_ERROR.value)
    print_code(f'logger.error("{LogMessage.BASIC_ERROR.value}")')
    
    print_info("\n  Sending ERROR log (timeout):")
    logger.error(LogMessage.TIMEOUT_ERROR.value)
    print_code(f'logger.error("{LogMessage.TIMEOUT_ERROR.value}")')
    
    print_info("\n✓ All log messages sent successfully")
    
    # SDK Commands Summary
    print_section("SDK Commands Summary")
    print_info("Commands used in this example:")
    print_code("1. initialize_telemetry(config, attrs, signal_types=['logging'])")
    print_code("2. get_telemetry_logger_handler()")
    print_code("3. logger.addHandler(handler)")
    print_code("4. logger.info/warning/error(message)")
    
    # Backend validation
    print_section("Backend Validation")
    print_info("To validate in backend:")
    print_info(f"  • Service Name: {SERVICE_NAME}")
    print_info(f"  • Service Version: {SERVICE_VERSION}")
    print_info("  • Expected 5 log messages:")
    print_info(f"    - INFO: {LogMessage.BASIC_INFO.value}")
    print_info(f"    - INFO: {LogMessage.USER_LOGOUT.value}")
    print_info(f"    - WARNING: {LogMessage.BASIC_WARNING.value}")
    print_info(f"    - ERROR: {LogMessage.BASIC_ERROR.value}")
    print_info(f"    - ERROR: {LogMessage.TIMEOUT_ERROR.value}")
    print_info("  • All logs should have resource attributes attached")
    
    # Flush logs to ensure they're sent to backend
    flush_logs()
    
    print_footer("✓ Example 8 completed successfully!")


if __name__ == "__main__":
    main()
