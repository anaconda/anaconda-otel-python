#!/usr/bin/env python3
"""
Example 9: Logging with Different Levels

Demonstrates using all Python logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
and how they are captured by the telemetry system.

WHEN TO USE THIS APPROACH:
- You need fine-grained control over log verbosity
- You want to filter logs by severity in your backend
- You need different log levels for different environments (dev vs prod)
- You want to track critical errors separately from informational logs

USE CASES:
- Development: Use DEBUG for detailed troubleshooting
- Production: Use INFO/WARNING for operational monitoring
- Alerting: Use ERROR/CRITICAL for automated alerts
- Compliance: Track all levels for audit trails
- Performance: Filter by level to reduce log volume

KEY CONCEPTS:
- Python logging levels: DEBUG < INFO < WARNING < ERROR < CRITICAL
- Log level can be set on the logger or in Configuration
- Lower levels include all higher severity levels
- Each level serves a specific purpose in application monitoring
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
    LogLevel,
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
    
    # Create configuration with DEBUG logging level
    print_section("1. Configure Logging Level")
    config = Configuration(default_endpoint=endpoint)
    apply_signal_specific_endpoints(config, endpoints)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    # Set logging level to DEBUG to capture all levels
    config.set_logging_level("DEBUG")
    print_code('config.set_logging_level("DEBUG")')
    print_info("✓ Logging level set to DEBUG (captures all levels)")
    
    # Create attributes
    attrs = ResourceAttributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Initialize with logging enabled
    print_section("2. Initialize Telemetry")
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['logging']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['logging'])")
    print_info("✓ Telemetry initialized")
    
    # Get handler and configure logger
    print_section("3. Configure Logger")
    handler = get_telemetry_logger_handler()
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    print_code(f'logger = logging.getLogger("{LOGGER_NAME}")')
    print_code("logger.setLevel(logging.DEBUG)")
    print_code("logger.addHandler(handler)")
    print_info("✓ Logger configured to capture all levels")
    
    # Demonstrate all logging levels
    print_section("4. Send Logs at All Levels")
    
    print_info("\n  Level 1: DEBUG (Lowest severity)")
    logger.debug(LogMessage.BASIC_DEBUG.value)
    print_code(f'logger.debug("{LogMessage.BASIC_DEBUG.value}")')
    print_info("    → Use for detailed troubleshooting information")
    
    print_info("\n  Level 2: INFO")
    logger.info(LogMessage.BASIC_INFO.value)
    print_code(f'logger.info("{LogMessage.BASIC_INFO.value}")')
    print_info("    → Use for general informational messages")
    
    print_info("\n  Level 3: WARNING")
    logger.warning(LogMessage.BASIC_WARNING.value)
    print_code(f'logger.warning("{LogMessage.BASIC_WARNING.value}")')
    print_info("    → Use for warning messages (non-critical issues)")
    
    print_info("\n  Level 4: ERROR")
    logger.error(LogMessage.BASIC_ERROR.value)
    print_code(f'logger.error("{LogMessage.BASIC_ERROR.value}")')
    print_info("    → Use for error messages (failures that need attention)")
    
    print_info("\n  Level 5: CRITICAL (Highest severity)")
    logger.critical(LogMessage.BASIC_CRITICAL.value)
    print_code(f'logger.critical("{LogMessage.BASIC_CRITICAL.value}")')
    print_info("    → Use for critical errors (system failures)")
    
    print_info("\n✓ All logging levels demonstrated")
    
    # Explain log level filtering
    print_section("5. Log Level Filtering")
    print_info("Understanding log level filtering:")
    print_info("  • If logger level = INFO:")
    print_info("    ✓ INFO, WARNING, ERROR, CRITICAL are captured")
    print_info("    ✗ DEBUG is filtered out")
    print_info("  • If logger level = WARNING:")
    print_info("    ✓ WARNING, ERROR, CRITICAL are captured")
    print_info("    ✗ DEBUG, INFO are filtered out")
    print_info("  • If logger level = DEBUG:")
    print_info("    ✓ All levels are captured (current setting)")
    
    # SDK Commands Summary
    print_section("SDK Commands Summary")
    print_info("Commands used in this example:")
    print_code("1. config.set_logging_level('DEBUG')")
    print_code("2. initialize_telemetry(config, attrs, signal_types=['logging'])")
    print_code("3. get_telemetry_logger_handler()")
    print_code("4. logger.debug/info/warning/error/critical(message)")
    
    # Backend validation
    print_section("Backend Validation")
    print_info("To validate in backend:")
    print_info(f"  • Service Name: {SERVICE_NAME}")
    print_info(f"  • Service Version: {SERVICE_VERSION}")
    print_info("  • Expected 5 log records with levels:")
    print_info(f"    - DEBUG: {LogMessage.BASIC_DEBUG.value}")
    print_info(f"    - INFO: {LogMessage.BASIC_INFO.value}")
    print_info(f"    - WARNING: {LogMessage.BASIC_WARNING.value}")
    print_info(f"    - ERROR: {LogMessage.BASIC_ERROR.value}")
    print_info(f"    - CRITICAL: {LogMessage.BASIC_CRITICAL.value}")
    print_info("  • Each log should have its severity level properly tagged")
    
    # Flush logs to ensure they're sent to backend
    flush_logs()
    
    print_footer("✓ Example 9 completed successfully!")


if __name__ == "__main__":
    main()
