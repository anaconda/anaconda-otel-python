#!/usr/bin/env python3
"""
Example 11: Multiple Loggers

Demonstrates using multiple named loggers with the same telemetry handler.
This is useful for organizing logs by component or module in your application.

WHEN TO USE MULTIPLE LOGGERS:
- Multiple modules/components in your application
- Filter logs by component in your backend
- Different log levels for different parts of your app
- Organize logs hierarchically (e.g., app.api, app.database)
"""

import logging
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
    LogAttributes,
    LoggerName,
    ServiceNameLogging
)

# Test data constants
SERVICE_NAME = ServiceNameLogging.LOGGING_MULTIPLE.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value


def main():
    print_header("Example 11: Multiple Loggers", 
                 "Use multiple named loggers for different components")
    
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
    config.set_logging_level("DEBUG")
    
    # Create attributes
    attrs = sdk.create_attributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Initialize with logging enabled
    print_section("1. Initialize Telemetry")
    sdk.initialize(config, attrs, signal_types=['logging'])
    
    # Create multiple loggers for different components
    print_section("2. Create Multiple Component Loggers")
    api_logger = sdk.get_logger(LoggerName.API_LOGGER.value, level=logging.INFO)
    db_logger = sdk.get_logger(LoggerName.DATABASE_LOGGER.value, level=logging.DEBUG)
    auth_logger = sdk.get_logger(LoggerName.AUTH_LOGGER.value, level=logging.WARNING)
    cache_logger = sdk.get_logger(LoggerName.CACHE_LOGGER.value, level=logging.INFO)
    custom_logger = sdk.get_logger(LoggerName.CUSTOM_LOGGER.value, level=logging.WARNING)
    
    # Use the loggers
    print_section("3. Use Different Loggers")
    api_logger.info(LogMessage.API_REQUEST.value, extra=LogAttributes.HTTP_REQUEST.value)
    api_logger.debug("API debug message")  # Filtered out (level < INFO)
    
    db_logger.debug("Executing database query")
    db_logger.info(LogMessage.DATABASE_QUERY.value, extra=LogAttributes.DB_QUERY.value)
    
    auth_logger.info("User authentication attempt")  # Filtered out (level < WARNING)
    auth_logger.warning(LogMessage.PERMISSION_DENIED.value, extra=LogAttributes.USER_WITH_ROLE.value)
    
    cache_logger.info(LogMessage.CACHE_HIT.value, extra=LogAttributes.CACHE_INFO.value)
    cache_logger.info(LogMessage.CACHE_MISS.value, extra=LogAttributes.CACHE_MISS_INFO.value)
    
    custom_logger.info("Custom info message")  # Filtered out (level < WARNING)
    custom_logger.warning(LogMessage.RATE_LIMIT.value, extra=LogAttributes.EMPTY.value)
    custom_logger.warning(LogMessage.HIGH_MEMORY.value)
    
    print_footer("✓ Example 11 completed successfully!")


if __name__ == "__main__":
    main()
