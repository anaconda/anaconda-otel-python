#!/usr/bin/env python3
"""
Example 11: Multiple Loggers

Demonstrates using multiple named loggers with the same telemetry handler.
This is useful for organizing logs by component or module in your application.

WHEN TO USE THIS APPROACH:
- You have multiple modules/components in your application
- You want to filter logs by component in your backend
- You need different log levels for different parts of your app
- You want to organize logs hierarchically (e.g., app.api, app.database)

USE CASES:
- Microservice with multiple components (API, database, cache, auth)
- Large applications with distinct modules
- Team-based development (different teams own different loggers)
- Debugging specific components without noise from others
- Different log levels per component (DEBUG for one, INFO for others)

KEY CONCEPTS:
- Python supports hierarchical logger names (e.g., 'app.api.users')
- Same telemetry handler can be added to multiple loggers
- Each logger can have its own log level
- Logger names appear in the telemetry data for filtering
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
SERVICE_NAME = ServiceNameLogging.LOGGING_MULTIPLE.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value


def main():
    print_header("Example 11: Multiple Loggers", 
                 "Use multiple named loggers for different components")
    
    # Load environment
    _, endpoint, use_console, endpoints = load_environment()
    print_environment_config(endpoint, use_console)
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    apply_signal_specific_endpoints(config, endpoints)
    if use_console:
        config.set_console_exporter(use_console=True)
    config.set_logging_level("DEBUG")
    
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
    
    # Get the shared telemetry handler
    print_section("2. Get Shared Telemetry Handler")
    handler = get_telemetry_logger_handler()
    print_code("handler = get_telemetry_logger_handler()")
    print_info("✓ Retrieved shared telemetry handler")
    
    # Create multiple loggers for different components
    print_section("3. Create Multiple Component Loggers")
    
    # API Logger
    api_logger = logging.getLogger(LoggerName.API_LOGGER.value)
    api_logger.setLevel(logging.INFO)
    api_logger.addHandler(handler)
    print_code(f'api_logger = logging.getLogger("{LoggerName.API_LOGGER.value}")')
    print_code("api_logger.setLevel(logging.INFO)")
    print_code("api_logger.addHandler(handler)")
    print_info(f"✓ API logger created: {LoggerName.API_LOGGER.value}")
    
    # Database Logger
    db_logger = logging.getLogger(LoggerName.DATABASE_LOGGER.value)
    db_logger.setLevel(logging.DEBUG)
    db_logger.addHandler(handler)
    print_code(f'db_logger = logging.getLogger("{LoggerName.DATABASE_LOGGER.value}")')
    print_code("db_logger.setLevel(logging.DEBUG)")
    print_code("db_logger.addHandler(handler)")
    print_info(f"✓ Database logger created: {LoggerName.DATABASE_LOGGER.value}")
    
    # Auth Logger
    auth_logger = logging.getLogger(LoggerName.AUTH_LOGGER.value)
    auth_logger.setLevel(logging.WARNING)
    auth_logger.addHandler(handler)
    print_code(f'auth_logger = logging.getLogger("{LoggerName.AUTH_LOGGER.value}")')
    print_code("auth_logger.setLevel(logging.WARNING)")
    print_code("auth_logger.addHandler(handler)")
    print_info(f"✓ Auth logger created: {LoggerName.AUTH_LOGGER.value}")
    
    # Cache Logger
    cache_logger = logging.getLogger(LoggerName.CACHE_LOGGER.value)
    cache_logger.setLevel(logging.INFO)
    cache_logger.addHandler(handler)
    print_code(f'cache_logger = logging.getLogger("{LoggerName.CACHE_LOGGER.value}")')
    print_code("cache_logger.setLevel(logging.INFO)")
    print_code("cache_logger.addHandler(handler)")
    print_info(f"✓ Cache logger created: {LoggerName.CACHE_LOGGER.value}")
    
    # Custom Logger (for specialized use cases)
    custom_logger = logging.getLogger(LoggerName.CUSTOM_LOGGER.value)
    custom_logger.setLevel(logging.WARNING)
    custom_logger.addHandler(handler)
    print_code(f'custom_logger = logging.getLogger("{LoggerName.CUSTOM_LOGGER.value}")')
    print_code("custom_logger.setLevel(logging.WARNING)")
    print_code("custom_logger.addHandler(handler)")
    print_info(f"✓ Custom logger created: {LoggerName.CUSTOM_LOGGER.value}")
    
    # Use the loggers
    print_section("4. Use Different Loggers")
    
    print_info("\n  API Logger (level: INFO):")
    api_logger.info(LogMessage.API_REQUEST.value, extra=LogAttributes.HTTP_REQUEST.value)
    print_code(f'api_logger.info("{LogMessage.API_REQUEST.value}", extra=...)')
    api_logger.debug("API debug message")  # This won't be captured (level too low)
    print_code('api_logger.debug("API debug message")  # Filtered out (level < INFO)')
    
    print_info("\n  Database Logger (level: DEBUG):")
    db_logger.debug("Executing database query")
    print_code('db_logger.debug("Executing database query")  # Captured (level >= DEBUG)')
    db_logger.info(LogMessage.DATABASE_QUERY.value, extra=LogAttributes.DB_QUERY.value)
    print_code(f'db_logger.info("{LogMessage.DATABASE_QUERY.value}", extra=...)')
    
    print_info("\n  Auth Logger (level: WARNING):")
    auth_logger.info("User authentication attempt")  # Won't be captured
    print_code('auth_logger.info("User authentication attempt")  # Filtered out (level < WARNING)')
    auth_logger.warning(LogMessage.PERMISSION_DENIED.value, extra=LogAttributes.USER_WITH_ROLE.value)
    print_code(f'auth_logger.warning("{LogMessage.PERMISSION_DENIED.value}", extra=...)')
    
    print_info("\n  Cache Logger (level: INFO):")
    cache_logger.info(LogMessage.CACHE_HIT.value, extra=LogAttributes.CACHE_INFO.value)
    print_code(f'cache_logger.info("{LogMessage.CACHE_HIT.value}", extra=...)')
    cache_logger.info(LogMessage.CACHE_MISS.value, extra=LogAttributes.CACHE_MISS_INFO.value)
    print_code(f'cache_logger.info("{LogMessage.CACHE_MISS.value}", extra=...)')
    
    print_info("\n  Custom Logger (level: WARNING):")
    custom_logger.info("Custom info message")  # Won't be captured
    print_code('custom_logger.info("Custom info message")  # Filtered out (level < WARNING)')
    custom_logger.warning(LogMessage.RATE_LIMIT.value, extra=LogAttributes.EMPTY.value)
    print_code(f'custom_logger.warning("{LogMessage.RATE_LIMIT.value}", extra=EMPTY)')
    custom_logger.warning(LogMessage.HIGH_MEMORY.value)
    print_code(f'custom_logger.warning("{LogMessage.HIGH_MEMORY.value}")')
    
    print_info("\n✓ All loggers used successfully")
    
    # Logger hierarchy explanation
    print_section("5. Logger Hierarchy and Naming")
    print_info("Logger naming best practices:")
    print_info("  • Use dot notation for hierarchy: 'app.api.users'")
    print_info("  • Parent loggers: 'app' is parent of 'app.api'")
    print_info("  • Child loggers inherit parent settings by default")
    print_info("  • Organize by component: api, database, auth, cache")
    print_info("  • Organize by feature: users, orders, payments")
    print_info("\nExample hierarchies:")
    print_info("  • app.api.users")
    print_info("  • app.api.orders")
    print_info("  • app.database.users")
    print_info("  • app.database.orders")
    
    # SDK Commands Summary
    print_section("SDK Commands Summary")
    print_info("Commands used in this example:")
    print_code("1. handler = get_telemetry_logger_handler()")
    print_code("2. logger1 = logging.getLogger('app.api')")
    print_code("3. logger1.addHandler(handler)")
    print_code("4. logger2 = logging.getLogger('app.database')")
    print_code("5. logger2.addHandler(handler)")
    print_code("6. logger1.info(message) / logger2.info(message)")
    
    # Backend validation
    print_section("Backend Validation")
    print_info("To validate in backend:")
    print_info(f"  • Service Name: {SERVICE_NAME}")
    print_info(f"  • Service Version: {SERVICE_VERSION}")
    print_info("  • Expected logs from different loggers:")
    print_info(f"    - {LoggerName.API_LOGGER.value}: 1 log (INFO level)")
    print_info(f"    - {LoggerName.DATABASE_LOGGER.value}: 2 logs (DEBUG and INFO)")
    print_info(f"    - {LoggerName.AUTH_LOGGER.value}: 1 log (WARNING level)")
    print_info(f"    - {LoggerName.CACHE_LOGGER.value}: 2 logs (INFO level)")
    print_info(f"    - {LoggerName.CUSTOM_LOGGER.value}: 2 logs (WARNING level)")
    print_info("  • Total: 8 log records")
    print_info("  • Each log should have logger name for filtering")
    print_info("  • Note: EMPTY attributes demonstrate logging without extra context")
    
    # Flush logs to ensure they're sent to backend
    flush_logs()
    
    print_footer("✓ Example 11 completed successfully!")


if __name__ == "__main__":
    main()
