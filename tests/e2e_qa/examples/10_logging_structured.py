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
    print_info("→ User activity with user.id and user.name")
    
    logger.info(LogMessage.API_REQUEST.value, extra=LogAttributes.HTTP_REQUEST.value)
    print_info("→ HTTP request with method, url, status_code")
    
    logger.info(LogMessage.DATABASE_QUERY.value, extra=LogAttributes.DB_QUERY.value)
    print_info("→ Database query with system, operation, table")
    
    logger.info("Operation completed", extra=LogAttributes.PERFORMANCE.value)
    print_info("→ Performance metrics with duration_ms, memory_mb")
    
    logger.error(LogMessage.CONNECTION_FAILED.value, extra=LogAttributes.ERROR_CONTEXT.value)
    print_info("→ Error with error.type and error.message")
    
    logger.info(LogMessage.CACHE_HIT.value, extra=LogAttributes.CACHE_INFO.value)
    print_info("→ Cache operation with cache.key and cache.hit")
    
    logger.info(LogMessage.USER_LOGIN.value, extra=LogAttributes.USER_WITH_EMAIL.value)
    print_info("→ User activity with email")
    
    logger.info(LogMessage.API_REQUEST.value, extra=LogAttributes.HTTP_POST.value)
    print_info("→ HTTP POST request")
    
    logger.error(LogMessage.API_REQUEST.value, extra=LogAttributes.HTTP_ERROR.value)
    print_info("→ HTTP error response")
    
    logger.info("Database insert operation", extra=LogAttributes.DB_INSERT.value)
    print_info("→ Database insert operation")
    
    logger.warning("Slow operation detected", extra=LogAttributes.SLOW_OPERATION.value)
    print_info("→ Slow operation warning")
    
    # Best practices
    print_section("4. Structured Logging Best Practices")
    print_info("Attribute naming conventions:")
    print_info("  • Use dot notation: 'user.id', 'http.method', 'db.system'")
    print_info("  • Be consistent: Same attribute names across logs")
    print_info("  • Be descriptive: 'duration_ms' not just 'time'")
    print_info("  • Group related: 'user.*', 'http.*', 'db.*'")
    
    print_footer("✓ Example 10 completed successfully!")


if __name__ == "__main__":
    main()
