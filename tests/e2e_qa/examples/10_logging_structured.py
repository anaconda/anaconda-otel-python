#!/usr/bin/env python3
"""
Example 10: Structured Logging with Attributes

Demonstrates structured logging by adding contextual attributes to log messages.
This enables better filtering, searching, and analysis in your telemetry backend.

WHEN TO USE THIS APPROACH:
- You need to add context to log messages (user IDs, request IDs, etc.)
- You want to filter logs by specific attributes in your backend
- You need to correlate logs with specific operations or users
- You want rich, searchable log data for analytics

USE CASES:
- User activity tracking (add user.id, user.name to logs)
- API request logging (add http.method, http.url, http.status_code)
- Database operation logging (add db.system, db.operation, db.table)
- Performance monitoring (add duration_ms, memory_mb)
- Error context (add error.type, error.message, stack traces)

KEY CONCEPTS:
- Python logging supports 'extra' parameter for additional attributes
- Attributes are sent as structured data to the backend
- Use consistent attribute naming for better searchability
- Attributes complement the log message with context
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
SERVICE_NAME = ServiceNameLogging.LOGGING_STRUCTURED.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
LOGGER_NAME = LoggerName.APP_LOGGER.value


def main():
    print_header("Example 10: Structured Logging with Attributes", 
                 "Add contextual attributes to log messages for better analysis")
    
    # Load environment
    _, endpoint, use_console, endpoints = load_environment()
    print_environment_config(endpoint, use_console)
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    apply_signal_specific_endpoints(config, endpoints)
    if use_console:
        config.set_console_exporter(use_console=True)
    config.set_logging_level("INFO")
    
    # Create attributes
    attrs = ResourceAttributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Initialize with logging enabled
    print_section("1. Initialize Telemetry")
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['logging']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['logging'])")
    print_info("✓ Telemetry initialized")
    
    # Get handler and configure logger
    print_section("2. Configure Logger")
    handler = get_telemetry_logger_handler()
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    print_info("✓ Logger configured")
    
    # Demonstrate structured logging with different attribute types
    print_section("3. Structured Logging Examples")
    
    # Example 1: User-related attributes
    print_info("\n  Example 1: User Activity Logging")
    user_attrs = LogAttributes.USER_BASIC.value
    logger.info(LogMessage.USER_LOGIN.value, extra=user_attrs)
    print_code(f'logger.info("{LogMessage.USER_LOGIN.value}", extra={user_attrs})')
    print_info(f"    → Attributes: {user_attrs}")
    
    # Example 2: HTTP request attributes
    print_info("\n  Example 2: HTTP Request Logging")
    http_attrs = LogAttributes.HTTP_REQUEST.value
    logger.info(LogMessage.API_REQUEST.value, extra=http_attrs)
    print_code(f'logger.info("{LogMessage.API_REQUEST.value}", extra={http_attrs})')
    print_info(f"    → Attributes: {http_attrs}")
    
    # Example 3: Database operation attributes
    print_info("\n  Example 3: Database Operation Logging")
    db_attrs = LogAttributes.DB_QUERY.value
    logger.info(LogMessage.DATABASE_QUERY.value, extra=db_attrs)
    print_code(f'logger.info("{LogMessage.DATABASE_QUERY.value}", extra={db_attrs})')
    print_info(f"    → Attributes: {db_attrs}")
    
    # Example 4: Performance attributes
    print_info("\n  Example 4: Performance Logging")
    perf_attrs = LogAttributes.PERFORMANCE.value
    logger.info("Operation completed", extra=perf_attrs)
    print_code(f'logger.info("Operation completed", extra={perf_attrs})')
    print_info(f"    → Attributes: {perf_attrs}")
    
    # Example 5: Error with context
    print_info("\n  Example 5: Error Logging with Context")
    error_attrs = LogAttributes.ERROR_CONTEXT.value
    logger.error(LogMessage.CONNECTION_FAILED.value, extra=error_attrs)
    print_code(f'logger.error("{LogMessage.CONNECTION_FAILED.value}", extra={error_attrs})')
    print_info(f"    → Attributes: {error_attrs}")
    
    # Example 6: Cache operation
    print_info("\n  Example 6: Cache Operation Logging")
    cache_attrs = LogAttributes.CACHE_INFO.value
    logger.info(LogMessage.CACHE_HIT.value, extra=cache_attrs)
    print_code(f'logger.info("{LogMessage.CACHE_HIT.value}", extra={cache_attrs})')
    print_info(f"    → Attributes: {cache_attrs}")
    
    # Example 7: User with email
    print_info("\n  Example 7: User Activity with Email")
    user_email_attrs = LogAttributes.USER_WITH_EMAIL.value
    logger.info(LogMessage.USER_LOGIN.value, extra=user_email_attrs)
    print_code(f'logger.info("{LogMessage.USER_LOGIN.value}", extra={user_email_attrs})')
    print_info(f"    → Attributes: {user_email_attrs}")
    
    # Example 8: HTTP POST request
    print_info("\n  Example 8: HTTP POST Request Logging")
    http_post_attrs = LogAttributes.HTTP_POST.value
    logger.info(LogMessage.API_REQUEST.value, extra=http_post_attrs)
    print_code(f'logger.info("{LogMessage.API_REQUEST.value}", extra={http_post_attrs})')
    print_info(f"    → Attributes: {http_post_attrs}")
    
    # Example 9: HTTP Error
    print_info("\n  Example 9: HTTP Error Logging")
    http_error_attrs = LogAttributes.HTTP_ERROR.value
    logger.error(LogMessage.API_REQUEST.value, extra=http_error_attrs)
    print_code(f'logger.error("{LogMessage.API_REQUEST.value}", extra={http_error_attrs})')
    print_info(f"    → Attributes: {http_error_attrs}")
    
    # Example 10: Database insert operation
    print_info("\n  Example 10: Database Insert Operation")
    db_insert_attrs = LogAttributes.DB_INSERT.value
    logger.info("Database insert operation", extra=db_insert_attrs)
    print_code(f'logger.info("Database insert operation", extra={db_insert_attrs})')
    print_info(f"    → Attributes: {db_insert_attrs}")
    
    # Example 11: Slow operation
    print_info("\n  Example 11: Slow Operation Logging")
    slow_op_attrs = LogAttributes.SLOW_OPERATION.value
    logger.warning("Slow operation detected", extra=slow_op_attrs)
    print_code(f'logger.warning("Slow operation detected", extra={slow_op_attrs})')
    print_info(f"    → Attributes: {slow_op_attrs}")
    
    print_info("\n✓ All structured log examples completed")
    
    # Best practices
    print_section("4. Structured Logging Best Practices")
    print_info("Attribute naming conventions:")
    print_info("  • Use dot notation: 'user.id', 'http.method', 'db.system'")
    print_info("  • Be consistent: Same attribute names across logs")
    print_info("  • Be descriptive: 'duration_ms' not just 'time'")
    print_info("  • Group related: 'user.*', 'http.*', 'db.*'")
    print_info("\nCommon attribute categories:")
    print_info("  • User context: user.id, user.name, user.role")
    print_info("  • HTTP context: http.method, http.url, http.status_code")
    print_info("  • Database context: db.system, db.operation, db.table")
    print_info("  • Error context: error.type, error.message, error.stack")
    print_info("  • Performance: duration_ms, memory_mb, cpu_percent")
    
    # SDK Commands Summary
    print_section("SDK Commands Summary")
    print_info("Commands used in this example:")
    print_code("1. initialize_telemetry(config, attrs, signal_types=['logging'])")
    print_code("2. get_telemetry_logger_handler()")
    print_code("3. logger.info(message, extra={'key': 'value'})")
    print_code("4. logger.error(message, extra={'error.type': 'ErrorType'})")
    
    # Backend validation
    print_section("Backend Validation")
    print_info("To validate in backend:")
    print_info(f"  • Service Name: {SERVICE_NAME}")
    print_info(f"  • Service Version: {SERVICE_VERSION}")
    print_info("  • Expected 11 log records with attributes:")
    print_info("    1. User login with user.id and user.name")
    print_info("    2. API request with http.method, http.url, http.status_code")
    print_info("    3. Database query with db.system, db.operation, db.table")
    print_info("    4. Performance log with duration_ms, memory_mb")
    print_info("    5. Error log with error.type, error.message")
    print_info("    6. Cache operation with cache.key, cache.hit")
    print_info("    7. User login with email")
    print_info("    8. HTTP POST request")
    print_info("    9. HTTP error response")
    print_info("    10. Database insert operation")
    print_info("    11. Slow operation warning")
    print_info("  • Each log should have its attributes searchable in backend")
    
    # Flush logs to ensure they're sent to backend
    flush_logs()
    
    print_footer("✓ Example 10 completed successfully!")


if __name__ == "__main__":
    main()
