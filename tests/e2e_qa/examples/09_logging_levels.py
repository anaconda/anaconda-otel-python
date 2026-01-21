#!/usr/bin/env python3
"""
Example 9: Logging with Different Levels

Demonstrates using all Python logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
and how they are captured by the telemetry system.

WHEN TO USE DIFFERENT LOG LEVELS:
- DEBUG: Detailed troubleshooting information (development)
- INFO: General informational messages (operational monitoring)
- WARNING: Non-critical issues that need attention
- ERROR: Failures that need immediate attention
- CRITICAL: System failures requiring urgent action
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
SERVICE_NAME = ServiceNameLogging.LOGGING_LEVELS.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
LOGGER_NAME = LoggerName.APP_LOGGER.value


def main():
    print_header("Example 9: Logging with Different Levels", 
                 "Demonstrate all Python logging levels with telemetry")
    
    # Load environment
    _, endpoint, use_console, endpoints = load_environment()
    print_environment_config(endpoint, use_console)
    
    # Initialize SDK operations wrapper
    sdk = SdkOperations(
        endpoint=endpoint,
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Create configuration with DEBUG logging level
    print_section("1. Configure Logging Level")
    config = sdk.create_configuration(endpoint=endpoint, use_console=use_console)
    sdk.apply_signal_specific_endpoints(config, endpoints)
    config.set_logging_level("DEBUG")
    print_info("→ Logging level set to DEBUG (captures all levels)")
    
    # Create attributes
    attrs = sdk.create_attributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Initialize with logging enabled
    print_section("2. Initialize Telemetry")
    sdk.initialize(config, attrs, signal_types=['logging'])
    
    # Get logger
    print_section("3. Setup Logger")
    logger = sdk.get_logger(LOGGER_NAME)
    print_info(f"→ Logger '{LOGGER_NAME}' configured to capture all levels")
    
    # Demonstrate all logging levels
    print_section("4. Send Logs at All Levels")
    
    logger.debug(LogMessage.BASIC_DEBUG.value)
    print_info("→ DEBUG: Detailed troubleshooting information")
    
    logger.info(LogMessage.BASIC_INFO.value)
    print_info("→ INFO: General informational messages")
    
    logger.warning(LogMessage.BASIC_WARNING.value)
    print_info("→ WARNING: Non-critical issues")
    
    logger.error(LogMessage.BASIC_ERROR.value)
    print_info("→ ERROR: Failures that need attention")
    
    logger.critical(LogMessage.BASIC_CRITICAL.value)
    print_info("→ CRITICAL: System failures")
    
    # Explain log level filtering
    print_section("5. Log Level Filtering")
    print_info("Understanding log level filtering:")
    print_info("  • DEBUG level: Captures all levels (current setting)")
    print_info("  • INFO level: Captures INFO, WARNING, ERROR, CRITICAL")
    print_info("  • WARNING level: Captures WARNING, ERROR, CRITICAL")
    print_info("  • ERROR level: Captures ERROR, CRITICAL")
    print_info("  • CRITICAL level: Captures only CRITICAL")
    
    print_footer("✓ Example 9 completed successfully!")


if __name__ == "__main__":
    main()
