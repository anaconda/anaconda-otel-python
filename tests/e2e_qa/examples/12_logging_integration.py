#!/usr/bin/env python3
"""
Example 12: Logging Integration with Metrics and Traces

Demonstrates using logging alongside metrics and traces to create comprehensive
observability. Shows how to correlate logs, metrics, and traces for the same operation.

WHEN TO USE INTEGRATED OBSERVABILITY:
- Complete observability (logs + metrics + traces)
- Correlate logs with metrics and traces
- Debug issues using multiple signal types
- Track both what happened (logs) and how it performed (metrics/traces)
"""

import logging
from anaconda.opentelemetry import (
    increment_counter,
    record_histogram,
    get_trace
)
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
SERVICE_NAME = ServiceNameLogging.LOGGING_INTEGRATION.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
LOGGER_NAME = LoggerName.APP_LOGGER.value


def simulate_api_request(logger):
    """Simulate an API request with logs, metrics, and traces."""
    with get_trace("api_request", attributes={"http.method": "GET", "http.url": "/api/users"}) as span:
        logger.info("API request started", extra={"http.method": "GET", "http.url": "/api/users"})
        
        span.add_event("validating_request")
        logger.debug("Validating request parameters")
        
        increment_counter("api_requests_total", by=1, attributes={"endpoint": "/api/users", "method": "GET"})
        
        span.add_event("database_query_start")
        logger.info("Executing database query", extra=LogAttributes.DB_QUERY.value)
        
        record_histogram("database_query_duration_ms", 45.5, attributes={"operation": "SELECT", "table": "users"})
        
        span.add_event("database_query_complete")
        logger.debug("Database query completed successfully")
        
        logger.info("API request completed", extra={"http.status_code": 200, "duration_ms": 50})
        
        increment_counter("api_requests_success", by=1, attributes={"endpoint": "/api/users"})


def simulate_error_scenario(logger):
    """Simulate an error scenario with logs, metrics, and traces."""
    with get_trace("api_request_error", attributes={"http.method": "POST", "http.url": "/api/orders"}) as span:
        logger.info("API request started", extra={"http.method": "POST", "http.url": "/api/orders"})
        
        span.add_event("validation_failed")
        logger.warning("Request validation failed", extra=LogAttributes.VALIDATION_ERROR.value)
        
        span.set_error_status("Validation error occurred")
        
        logger.error(LogMessage.VALIDATION_ERROR.value, extra=LogAttributes.VALIDATION_ERROR.value)
        
        increment_counter("api_requests_errors", by=1, attributes={"endpoint": "/api/orders", "error_type": "ValidationError"})
        
        record_histogram("api_request_duration_ms", 15.0, attributes={"endpoint": "/api/orders", "status": "error"})


def simulate_multi_service_scenario(sdk):
    """Simulate multiple services with separate loggers."""
    service1_logger = sdk.get_logger(LoggerName.MULTIPLE_LOGGER_1.value)
    service2_logger = sdk.get_logger(LoggerName.MULTIPLE_LOGGER_2.value)
    service3_logger = sdk.get_logger(LoggerName.MULTIPLE_LOGGER_3.value)
    
    with get_trace("multi_service_operation", attributes={"operation": "distributed_task"}) as span:
        service1_logger.info("Service 1 processing started")
        span.add_event("service1_started")
        increment_counter("service_operations", by=1, attributes={"service": "service1"})
        
        service2_logger.info("Service 2 processing data")
        span.add_event("service2_processing")
        increment_counter("service_operations", by=1, attributes={"service": "service2"})
        
        service3_logger.info("Service 3 finalizing results")
        span.add_event("service3_finalizing")
        increment_counter("service_operations", by=1, attributes={"service": "service3"})
        
        record_histogram("multi_service_duration_ms", 120.0, attributes={"services": "3"})


def main():
    print_header("Example 12: Logging Integration with Metrics and Traces", 
                 "Comprehensive observability with all three signal types")
    
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
    
    # Initialize with all signals
    print_section("1. Initialize All Signal Types")
    sdk.initialize(config, attrs, signal_types=['logging', 'metrics', 'tracing'])
    print_info("→ Logging, Metrics, and Tracing enabled")
    
    # Get logger
    print_section("2. Setup Logger")
    logger = sdk.get_logger(LOGGER_NAME)
    
    # Scenario 1: Successful API request
    print_section("3. Scenario 1: Successful API Request")
    simulate_api_request(logger)
    print_info("→ Logs, metrics, and traces captured for successful request")
    
    # Scenario 2: Error scenario
    print_section("4. Scenario 2: Error Scenario")
    simulate_error_scenario(logger)
    print_info("→ Error logs, metrics, and traces with error status captured")
    
    # Scenario 3: Multi-service coordination
    print_section("5. Scenario 3: Multi-Service Coordination")
    simulate_multi_service_scenario(sdk)
    print_info("→ Multiple service loggers coordinated with traces and metrics")
    
    # Correlation explanation
    print_section("6. Signal Correlation")
    print_info("How signals correlate:")
    print_info("  • session.id: Same for all signals in this run")
    print_info("  • Resource attributes: Attached to all signals")
    print_info("  • Timestamps: Correlate events in time")
    print_info("  • Custom attributes: Link related events")
    
    # Use cases
    print_section("7. Real-World Use Cases")
    print_info("Debugging with multiple signals:")
    print_info("  • Trace shows: Operation took 5 seconds (slow)")
    print_info("  • Logs show: Database query timeout occurred")
    print_info("  • Metrics show: Database query latency spiked")
    print_info("  → Conclusion: Database performance issue")
    
    print_footer("✓ Example 12 completed successfully!")


if __name__ == "__main__":
    main()
