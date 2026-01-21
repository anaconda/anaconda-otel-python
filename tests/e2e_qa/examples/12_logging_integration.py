#!/usr/bin/env python3
"""
Example 12: Logging Integration with Metrics and Traces

Demonstrates using logging alongside metrics and traces to create comprehensive
observability. Shows how to correlate logs, metrics, and traces for the same operation.

WHEN TO USE THIS APPROACH:
- You need complete observability (logs + metrics + traces)
- You want to correlate logs with metrics and traces
- You need to debug issues using multiple signal types
- You want to track both what happened (logs) and how it performed (metrics/traces)

USE CASES:
- Production monitoring: Track errors (logs), performance (metrics), and flows (traces)
- Debugging: Use traces to find slow operations, logs for details, metrics for trends
- SLO monitoring: Combine metrics for SLIs with logs for context
- Incident response: Correlate all signals to understand root cause
- Performance optimization: Traces show bottlenecks, logs show why, metrics show impact

KEY CONCEPTS:
- All three signal types share the same session.id for correlation
- Resource attributes are attached to all signals
- Logs provide details, metrics provide trends, traces provide flows
- Use consistent naming and attributes across signals
"""

import logging
from anaconda.opentelemetry import (
    Configuration, 
    ResourceAttributes, 
    initialize_telemetry,
    increment_counter,
    record_histogram,
    get_trace
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
    flush_telemetry,
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
SERVICE_NAME = ServiceNameLogging.LOGGING_INTEGRATION.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value
LOGGER_NAME = LoggerName.APP_LOGGER.value


def simulate_api_request():
    """
    Simulate an API request with logs, metrics, and traces.
    """
    # Get logger
    logger = logging.getLogger(LOGGER_NAME)
    
    # Create a trace for the operation
    with get_trace("api_request", attributes={"http.method": "GET", "http.url": "/api/users"}) as span:
        # Log the start of the request
        logger.info("API request started", extra={"http.method": "GET", "http.url": "/api/users"})
        
        # Simulate some work and add trace event
        span.add_event("validating_request")
        logger.debug("Validating request parameters")
        
        # Increment request counter
        increment_counter("api_requests_total", by=1, attributes={"endpoint": "/api/users", "method": "GET"})
        
        # Simulate database query
        span.add_event("database_query_start")
        logger.info("Executing database query", extra=LogAttributes.DB_QUERY.value)
        
        # Record query duration
        record_histogram("database_query_duration_ms", 45.5, attributes={"operation": "SELECT", "table": "users"})
        
        span.add_event("database_query_complete")
        logger.debug("Database query completed successfully")
        
        # Log successful response
        logger.info("API request completed", extra={"http.status_code": 200, "duration_ms": 50})
        
        # Increment success counter
        increment_counter("api_requests_success", by=1, attributes={"endpoint": "/api/users"})


def simulate_error_scenario():
    """
    Simulate an error scenario with logs, metrics, and traces.
    """
    logger = logging.getLogger(LOGGER_NAME)
    
    with get_trace("api_request_error", attributes={"http.method": "POST", "http.url": "/api/orders"}) as span:
        logger.info("API request started", extra={"http.method": "POST", "http.url": "/api/orders"})
        
        # Simulate an error
        span.add_event("validation_failed")
        logger.warning("Request validation failed", extra=LogAttributes.VALIDATION_ERROR.value)
        
        # Set error status on span
        span.set_error_status("Validation error occurred")
        
        # Log the error
        logger.error(LogMessage.VALIDATION_ERROR.value, extra=LogAttributes.VALIDATION_ERROR.value)
        
        # Increment error counter
        increment_counter("api_requests_errors", by=1, attributes={"endpoint": "/api/orders", "error_type": "ValidationError"})
        
        # Record error response time
        record_histogram("api_request_duration_ms", 15.0, attributes={"endpoint": "/api/orders", "status": "error"})


def simulate_multi_service_scenario():
    """
    Simulate multiple services logging with different loggers.
    Demonstrates how different components can use separate loggers.
    """
    # Create separate loggers for different services
    service1_logger = logging.getLogger(LoggerName.MULTIPLE_LOGGER_1.value)
    service1_logger.setLevel(logging.INFO)
    service1_logger.addHandler(get_telemetry_logger_handler())
    
    service2_logger = logging.getLogger(LoggerName.MULTIPLE_LOGGER_2.value)
    service2_logger.setLevel(logging.INFO)
    service2_logger.addHandler(get_telemetry_logger_handler())
    
    service3_logger = logging.getLogger(LoggerName.MULTIPLE_LOGGER_3.value)
    service3_logger.setLevel(logging.INFO)
    service3_logger.addHandler(get_telemetry_logger_handler())
    
    # Simulate coordinated operation across services
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
    
    # Initialize with all signals
    print_section("1. Initialize All Signal Types")
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['logging', 'metrics', 'tracing']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['logging', 'metrics', 'tracing'])")
    print_info("✓ Telemetry initialized with all signals")
    print_info("  • Logging: Enabled")
    print_info("  • Metrics: Enabled")
    print_info("  • Tracing: Enabled")
    
    # Configure logger
    print_section("2. Configure Logger")
    handler = get_telemetry_logger_handler()
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    print_info("✓ Logger configured")
    
    # Scenario 1: Successful API request
    print_section("3. Scenario 1: Successful API Request")
    print_info("Simulating successful API request with logs, metrics, and traces...")
    print_code("with get_trace('api_request', ...) as span:")
    print_code("    logger.info('API request started', ...)")
    print_code("    increment_counter('api_requests_total', ...)")
    print_code("    logger.info('Executing database query', ...)")
    print_code("    record_histogram('database_query_duration_ms', ...)")
    print_code("    logger.info('API request completed', ...)")
    
    simulate_api_request()
    print_info("✓ Successful request scenario completed")
    
    # Scenario 2: Error scenario
    print_section("4. Scenario 2: Error Scenario")
    print_info("Simulating error scenario with logs, metrics, and traces...")
    print_code("with get_trace('api_request_error', ...) as span:")
    print_code("    logger.warning('Request validation failed', ...)")
    print_code("    span.set_error_status('Validation error occurred')")
    print_code("    logger.error('Validation error', ...)")
    print_code("    increment_counter('api_requests_errors', ...)")
    
    simulate_error_scenario()
    print_info("✓ Error scenario completed")
    
    # Scenario 3: Multi-service coordination
    print_section("5. Scenario 3: Multi-Service Coordination")
    print_info("Simulating multiple services with separate loggers...")
    print_code("service1_logger = logging.getLogger('app.service1')")
    print_code("service2_logger = logging.getLogger('app.service2')")
    print_code("service3_logger = logging.getLogger('app.service3')")
    print_code("with get_trace('multi_service_operation', ...) as span:")
    print_code("    service1_logger.info('Service 1 processing started')")
    print_code("    service2_logger.info('Service 2 processing data')")
    print_code("    service3_logger.info('Service 3 finalizing results')")
    
    simulate_multi_service_scenario()
    print_info("✓ Multi-service scenario completed")
    
    # Correlation explanation
    print_section("6. Signal Correlation")
    print_info("How signals correlate:")
    print_info("  • session.id: Same for all signals in this run")
    print_info("  • Resource attributes: Attached to all signals")
    print_info("  • Timestamps: Correlate events in time")
    print_info("  • Custom attributes: Link related events")
    print_info("\nQuerying correlated data:")
    print_info("  1. Find trace by span name or attributes")
    print_info("  2. Get session.id from trace")
    print_info("  3. Query logs with same session.id")
    print_info("  4. Query metrics with same session.id")
    print_info("  5. Analyze together for complete picture")
    
    # Use cases
    print_section("7. Real-World Use Cases")
    print_info("Debugging with multiple signals:")
    print_info("  • Trace shows: Operation took 5 seconds (slow)")
    print_info("  • Logs show: Database query timeout occurred")
    print_info("  • Metrics show: Database query latency spiked")
    print_info("  → Conclusion: Database performance issue")
    print_info("\nMonitoring with multiple signals:")
    print_info("  • Metrics show: Error rate increased to 5%")
    print_info("  • Logs show: Validation errors for specific field")
    print_info("  • Traces show: Errors occur in validation step")
    print_info("  → Conclusion: Input validation needs fixing")
    
    # SDK Commands Summary
    print_section("SDK Commands Summary")
    print_info("Commands used in this example:")
    print_code("1. initialize_telemetry(config, attrs, signal_types=['logging', 'metrics', 'tracing'])")
    print_code("2. get_telemetry_logger_handler()")
    print_code("3. logger.info/warning/error(message, extra={...})")
    print_code("4. increment_counter(name, by=1, attributes={...})")
    print_code("5. record_histogram(name, value, attributes={...})")
    print_code("6. with get_trace(name, attributes={...}) as span:")
    print_code("7.     span.add_event(name)")
    print_code("8.     span.set_error_status(message)")
    
    # Backend validation
    print_section("Backend Validation")
    print_info("To validate in backend:")
    print_info(f"  • Service Name: {SERVICE_NAME}")
    print_info(f"  • Service Version: {SERVICE_VERSION}")
    print_info("  • Expected signals:")
    print_info("    Logs: ~13 log records (info, debug, warning, error)")
    print_info("      - From app.main logger")
    print_info("      - From app.service1, app.service2, app.service3 loggers")
    print_info("    Metrics: 6 metrics")
    print_info("      - api_requests_total (counter)")
    print_info("      - api_requests_success (counter)")
    print_info("      - api_requests_errors (counter)")
    print_info("      - service_operations (counter, 3 instances)")
    print_info("      - database_query_duration_ms (histogram)")
    print_info("      - api_request_duration_ms (histogram)")
    print_info("      - multi_service_duration_ms (histogram)")
    print_info("    Traces: 3 traces")
    print_info("      - api_request (successful)")
    print_info("      - api_request_error (with error status)")
    print_info("      - multi_service_operation (coordinated services)")
    print_info("  • All signals share the same session.id")
    print_info("  • Use session.id to correlate all signals")
    print_info("  • Different logger names allow filtering by component")
    
    # Flush all telemetry (logs, metrics, traces) to ensure they're sent to backend
    flush_telemetry()
    
    print_footer("✓ Example 12 completed successfully!")


if __name__ == "__main__":
    main()
