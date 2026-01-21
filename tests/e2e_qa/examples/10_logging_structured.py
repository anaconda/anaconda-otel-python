#!/usr/bin/env python3
"""
Example 10: Structured Logging with Attributes

Demonstrates structured logging by adding contextual attributes to log messages.
This enables better filtering, searching, and analysis in your telemetry backend.

WHEN TO USE STRUCTURED LOGGING:
- Add context to log messages (user IDs, request IDs, etc.)
- Filter logs by specific attributes in your backend
- Correlate logs with specific operations or users
- Track performance metrics with logs
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
    LogAttributes,
    LoggerName,
    ServiceNameLogging
)

# Test data constants
SERVICE_NAME = ServiceNameLogging.LOGGING_STRUCTURED.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
LOGGER_NAME = LoggerName.APP_LOGGER.value


def main():
    print_header("Example 10: Structured Logging with Attributes", 
                 "Add contextual attributes to log messages for better analysis")
    
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
    config.set_logging_level("INFO")
    
    # Create attributes
    attrs = sdk.create_attributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Initialize with logging enabled
    print_section("1. Initialize Telemetry")
    sdk.initialize(config, attrs, signal_types=['logging'])
    
    # Get logger
    print_section("2. Setup Logger")
    logger = sdk.get_logger(LOGGER_NAME)
    
    # Demonstrate structured logging with different attribute types
    print_section("3. Structured Logging Examples")
    logger.info(LogMessage.USER_LOGIN.value, extra=LogAttributes.USER_BASIC.value)
    logger.info(LogMessage.API_REQUEST.value, extra=LogAttributes.HTTP_REQUEST.value)
    logger.info(LogMessage.DATABASE_QUERY.value, extra=LogAttributes.DB_QUERY.value)
    logger.info("Operation completed", extra=LogAttributes.PERFORMANCE.value)
    logger.error(LogMessage.CONNECTION_FAILED.value, extra=LogAttributes.ERROR_CONTEXT.value)
    logger.info(LogMessage.CACHE_HIT.value, extra=LogAttributes.CACHE_INFO.value)
    logger.info(LogMessage.USER_LOGIN.value, extra=LogAttributes.USER_WITH_EMAIL.value)
    logger.info(LogMessage.API_REQUEST.value, extra=LogAttributes.HTTP_POST.value)
    logger.error(LogMessage.API_REQUEST.value, extra=LogAttributes.HTTP_ERROR.value)
    logger.info("Database insert operation", extra=LogAttributes.DB_INSERT.value)
    logger.warning("Slow operation detected", extra=LogAttributes.SLOW_OPERATION.value)
    
    print_footer("✓ Example 10 completed successfully!")


if __name__ == "__main__":
    main()
