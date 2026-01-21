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
"""

from utils import (
    load_environment,
    print_header,
    print_footer,
    print_info,
    print_section,
    print_environment_config,
    SdkOperations,
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
    
    # Initialize SDK operations wrapper
    sdk = SdkOperations(
        endpoint=endpoint,
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Create configuration
    config = sdk.create_configuration(endpoint=endpoint, use_console=use_console)
    sdk.apply_signal_specific_endpoints(config, endpoints)
    
    # Create attributes
    attrs = sdk.create_attributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Initialize with logging enabled
    print_section("1. Initialize Telemetry")
    sdk.initialize(config, attrs, signal_types=['logging'])
    
    # Get the telemetry logger and send log messages
    print_section("2. Setup Logger and Send Messages")
    logger = sdk.get_logger(LOGGER_NAME)
    print_info(f"→ Logger '{LOGGER_NAME}' configured with telemetry handler")
    
    # Send log messages at different levels
    print_section("3. Send Log Messages at Different Levels")
    logger.info(LogMessage.BASIC_INFO.value)
    logger.info(LogMessage.USER_LOGOUT.value)
    print_info("→ Sent INFO level logs")
    
    logger.warning(LogMessage.BASIC_WARNING.value)
    print_info("→ Sent WARNING level log")
    
    logger.error(LogMessage.BASIC_ERROR.value)
    logger.error(LogMessage.TIMEOUT_ERROR.value)
    print_info("→ Sent ERROR level logs")
    
    print_footer("✓ Example 8 completed successfully!")


if __name__ == "__main__":
    main()
