#!/usr/bin/env python3
"""
Example 13: Logging with Explicit Flush

Demonstrates explicit flush functionality for logging to ensure telemetry data
is sent before the application exits.

WHEN TO USE EXPLICIT FLUSH:
- Short-lived processes or scripts that need guaranteed log delivery
- Lambda functions or serverless applications
- Testing and validation scenarios where you need to confirm logs were sent
- Applications that need to ensure logs are exported before shutdown

NOTE: Python SDK automatically flushes on process exit. Explicit flush is useful
for immediate export or ensuring data is sent before continuing execution.
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
SERVICE_NAME = ServiceNameLogging.LOGGING_FLUSH.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
LOGGER_NAME = LoggerName.APP_LOGGER.value


def main():
    print_header("Example 13: Logging with Explicit Flush", 
                 "Verify flush functionality for logging doesn't break telemetry flow")
    
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
    
    # Get logger
    print_section("2. Setup Logger")
    logger = sdk.get_logger(LOGGER_NAME)
    
    # Send multiple log messages
    print_section("3. Send Log Messages")
    logger.info(LogMessage.USER_LOGIN.value, extra=LogAttributes.USER_BASIC.value)
    logger.warning(LogMessage.SLOW_QUERY.value, extra=LogAttributes.DB_SLOW_QUERY.value)
    logger.error(LogMessage.CONNECTION_FAILED.value, extra=LogAttributes.ERROR_CONTEXT.value)
    print_info("→ Sent INFO, WARNING, and ERROR logs")
    
    # Explicit flush
    print_section("4. Explicit Flush")
    sdk.flush_logs()
    print_info("→ Flush completed successfully")
    print_info("\nNote: Python SDK automatically flushes on process exit.")
    print_info("Explicit flush is useful for:")
    print_info("  • Short-lived processes (Lambda, CLI tools)")
    print_info("  • Testing and validation")
    print_info("  • Ensuring logs are sent before continuing")
    
    print_footer("✓ Example 13 completed successfully!")


if __name__ == "__main__":
    main()
