# E2E QA Project - Test Scenarios

## Overview

This document details all test scenarios that will be implemented in the E2E QA project. Each scenario demonstrates specific SDK functionality and validates correct behavior.

---

## 1. Configuration Scenarios

### 1.1 Basic Configuration
**Objective**: Demonstrate basic endpoint configuration

**Example Code**:
```python
def basic_configuration_example():
    """Create basic configuration with default endpoint"""
    config = Configuration(default_endpoint='http://localhost:4318')
    return config
```

**Validation**:
- Configuration object is created successfully
- Default endpoint is set correctly
- No errors are raised

---

### 1.2 Console Exporter Configuration
**Objective**: Demonstrate console exporter setup for local testing

**Example Code**:
```python
def console_exporter_example():
    """Configure console exporter for local testing"""
    config = Configuration(default_endpoint='http://localhost:4318')
    config.set_console_exporter(use_console=True)
    return config
```

**Validation**:
- Console exporter is enabled
- Configuration is valid

---

### 1.3 Signal-Specific Endpoints
**Objective**: Demonstrate different endpoints for different signals

**Example Code**:
```python
def signal_specific_endpoints_example():
    """Configure different endpoints for each signal type"""
    config = Configuration(default_endpoint='http://localhost:4318')
    config.set_metrics_endpoint('http://metrics.example.com:4318')
    config.set_logging_endpoint('http://logs.example.com:4318')
    config.set_tracing_endpoint('http://traces.example.com:4318')
    return config
```

**Validation**:
- Each signal has correct endpoint
- Endpoints are properly formatted

---

### 1.4 Export Intervals
**Objective**: Demonstrate configuring export intervals

**Example Code**:
```python
def export_intervals_example():
    """Configure custom export intervals"""
    config = Configuration(default_endpoint='http://localhost:4318')
    config.set_metrics_export_interval_ms(30000)  # 30 seconds
    config.set_tracing_export_interval_ms(15000)  # 15 seconds
    return config
```

**Validation**:
- Export intervals are set correctly
- Values are in milliseconds

---

### 1.5 Session Entropy
**Objective**: Demonstrate session ID entropy configuration

**Example Code**:
```python
def session_entropy_example():
    """Configure session entropy for consistent session IDs"""
    import time
    entropy = time.time()
    config = Configuration(default_endpoint='http://localhost:4318')
    config.set_tracing_session_entropy(entropy)
    return config
```

**Validation**:
- Session entropy is set
- Session ID will be deterministic

---

### 1.6 Logging Level Configuration
**Objective**: Demonstrate logging level setup

**Example Code**:
```python
def logging_level_example():
    """Configure logging level for telemetry"""
    config = Configuration(default_endpoint='http://localhost:4318')
    config.set_logging_level('warning')
    return config
```

**Validation**:
- Logging level is set correctly
- Valid levels: debug, info, warning, error, critical

---

## 2. Resource Attributes Scenarios

### 2.1 Basic Attributes
**Objective**: Demonstrate basic resource attributes creation

**Example Code**:
```python
def basic_attributes_example():
    """Create basic resource attributes"""
    attrs = ResourceAttributes(
        service_name="hello-world-service",
        service_version="1.0.0"
    )
    return attrs
```

**Validation**:
- Attributes object created
- Required fields are set
- Auto-populated fields (os_type, hostname) are present

---

### 2.2 Custom Attributes
**Objective**: Demonstrate setting custom attributes

**Example Code**:
```python
def custom_attributes_example():
    """Set custom attributes using set_attributes()"""
    attrs = ResourceAttributes("hello-world-service", "1.0.0")
    attrs.set_attributes(
        environment="production",
        platform="aws",
        region="us-west-2",
        custom_field="custom_value"
    )
    return attrs
```

**Validation**:
- Custom attributes are set
- Both common and dynamic attributes work
- Parameters dictionary contains custom fields

---

### 2.3 Environment-Specific Attributes
**Objective**: Demonstrate environment-aware attributes

**Example Code**:
```python
def environment_attributes_example():
    """Set environment-specific attributes"""
    attrs = ResourceAttributes("hello-world-service", "1.0.0")
    attrs.set_attributes(
        environment="development",
        hostname="dev-machine-001",
        platform="local"
    )
    return attrs
```

**Validation**:
- Environment is set correctly
- Valid environments: test, development, staging, production

---

## 3. Initialization Scenarios

### 3.1 Full Initialization
**Objective**: Initialize with all signal types

**Example Code**:
```python
def full_initialization_example():
    """Initialize telemetry with all signals"""
    config = Configuration(default_endpoint='http://localhost:4318')
    config.set_console_exporter(use_console=True)
    
    attrs = ResourceAttributes("hello-world-service", "1.0.0")
    
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['logging', 'metrics', 'tracing']
    )
    return True
```

**Validation**:
- Initialization succeeds
- All signals are initialized
- No errors are raised

---

### 3.2 Selective Signal Initialization
**Objective**: Initialize only specific signals

**Example Code**:
```python
def selective_initialization_example():
    """Initialize only metrics and tracing"""
    config = Configuration(default_endpoint='http://localhost:4318')
    config.set_console_exporter(use_console=True)
    
    attrs = ResourceAttributes("hello-world-service", "1.0.0")
    
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics', 'tracing']  # No logging
    )
    return True
```

**Validation**:
- Only specified signals are initialized
- Logging is not available

---

### 3.3 Default Initialization
**Objective**: Initialize with default settings (metrics only)

**Example Code**:
```python
def default_initialization_example():
    """Initialize with default signal types"""
    config = Configuration(default_endpoint='http://localhost:4318')
    config.set_console_exporter(use_console=True)
    
    attrs = ResourceAttributes("hello-world-service", "1.0.0")
    
    initialize_telemetry(config=config, attributes=attrs)
    # Default: signal_types=['metrics']
    return True
```

**Validation**:
- Only metrics are initialized by default
- Logging and tracing are not available

---

## 4. Logging Scenarios

### 4.1 Basic Logging
**Objective**: Demonstrate basic log message export

**Example Code**:
```python
def basic_logging_example():
    """Send basic log messages"""
    # Setup
    config = Configuration(default_endpoint='http://localhost:4318')
    config.set_console_exporter(use_console=True)
    attrs = ResourceAttributes("hello-world-service", "1.0.0")
    initialize_telemetry(config, attrs, signal_types=['logging'])
    
    # Get logger
    import logging
    logger = logging.getLogger(__name__)
    logger.addHandler(get_telemetry_logger_handler())
    
    # Send logs
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    return True
```

**Validation**:
- Logs appear in console output
- Log levels are correct
- Timestamps are present

---

### 4.2 Structured Logging
**Objective**: Demonstrate logging with context

**Example Code**:
```python
def structured_logging_example():
    """Send structured log messages"""
    # Setup (same as above)
    
    logger.info("User logged in", extra={
        "user_id": "user123",
        "session_id": "session456"
    })
    
    return True
```

**Validation**:
- Extra fields appear in log output
- Log structure is preserved

---

## 5. Metrics Scenarios

### 5.1 Counter Increment
**Objective**: Demonstrate counter increment

**Example Code**:
```python
def counter_increment_example():
    """Increment a counter metric"""
    # Setup
    config = Configuration(default_endpoint='http://localhost:4318')
    config.set_console_exporter(use_console=True)
    attrs = ResourceAttributes("hello-world-service", "1.0.0")
    initialize_telemetry(config, attrs, signal_types=['metrics'])
    
    # Increment counter
    result = increment_counter(
        "user_login_count",
        by=1,
        attributes={"user_id": "user123", "method": "oauth"}
    )
    
    return result
```

**Validation**:
- Counter increments successfully
- Attributes are attached
- Console shows metric data

---

### 5.2 Counter Decrement
**Objective**: Demonstrate up/down counter decrement

**Example Code**:
```python
def counter_decrement_example():
    """Decrement an up/down counter"""
    # Setup (same as above)
    
    # First increment to create counter
    increment_counter("active_connections", by=5)
    
    # Then decrement
    result = decrement_counter(
        "active_connections",
        by=2,
        attributes={"server": "server-01"}
    )
    
    return result
```

**Validation**:
- Counter decrements successfully
- Up/down counter is created
- Final value reflects decrement

---

### 5.3 Histogram Recording
**Objective**: Demonstrate histogram metric

**Example Code**:
```python
def histogram_example():
    """Record histogram values"""
    # Setup (same as above)
    
    # Record multiple values
    record_histogram(
        "request_duration_ms",
        value=123.45,
        attributes={"endpoint": "/api/users", "method": "GET"}
    )
    
    record_histogram(
        "request_duration_ms",
        value=234.56,
        attributes={"endpoint": "/api/users", "method": "POST"}
    )
    
    return True
```

**Validation**:
- Histogram values are recorded
- Distribution is created
- Attributes differentiate data points

---

### 5.4 Multiple Metrics
**Objective**: Demonstrate multiple metric types together

**Example Code**:
```python
def multiple_metrics_example():
    """Use multiple metric types together"""
    # Setup (same as above)
    
    # Counter for requests
    increment_counter("http_requests_total", by=1)
    
    # Histogram for duration
    record_histogram("http_request_duration_seconds", value=0.234)
    
    # Up/down counter for active connections
    increment_counter("active_connections", by=1)
    
    return True
```

**Validation**:
- All metrics are recorded
- Different metric types coexist
- Console shows all metrics

---

## 6. Tracing Scenarios

### 6.1 Basic Trace
**Objective**: Demonstrate basic trace context manager

**Example Code**:
```python
def basic_trace_example():
    """Create a basic trace"""
    # Setup
    config = Configuration(default_endpoint='http://localhost:4318')
    config.set_console_exporter(use_console=True)
    attrs = ResourceAttributes("hello-world-service", "1.0.0")
    initialize_telemetry(config, attrs, signal_types=['tracing'])
    
    # Create trace
    with get_trace("user_request", attributes={"user_id": "user123"}):
        # Simulate work
        import time
        time.sleep(0.1)
    
    return True
```

**Validation**:
- Trace is created and closed
- Span duration is recorded
- Attributes are attached

---

### 6.2 Span Events
**Objective**: Demonstrate adding events to spans

**Example Code**:
```python
def span_events_example():
    """Add events to a span"""
    # Setup (same as above)
    
    with get_trace("process_order") as span:
        span.add_event("order_validated", attributes={"order_id": "order123"})
        
        # Simulate processing
        import time
        time.sleep(0.05)
        
        span.add_event("payment_processed", attributes={"amount": 99.99})
        
        time.sleep(0.05)
        
        span.add_event("order_completed")
    
    return True
```

**Validation**:
- Events appear in span
- Event timestamps are sequential
- Event attributes are preserved

---

### 6.3 Span Exceptions
**Objective**: Demonstrate exception handling in spans

**Example Code**:
```python
def span_exception_example():
    """Handle exceptions in spans"""
    # Setup (same as above)
    
    with get_trace("risky_operation") as span:
        try:
            # Simulate error
            raise ValueError("Something went wrong")
        except Exception as e:
            span.add_exception(e)
            span.set_error_status("Operation failed")
    
    return True
```

**Validation**:
- Exception is recorded in span
- Error status is set
- Span completes successfully

---

### 6.4 Span Attributes
**Objective**: Demonstrate adding attributes to spans

**Example Code**:
```python
def span_attributes_example():
    """Add attributes to spans dynamically"""
    # Setup (same as above)
    
    with get_trace("database_query") as span:
        # Add initial attributes
        span.add_attributes({"query_type": "SELECT"})
        
        # Simulate query
        import time
        time.sleep(0.05)
        
        # Add result attributes
        span.add_attributes({
            "rows_returned": 42,
            "duration_ms": 50
        })
    
    return True
```

**Validation**:
- Attributes are added to span
- Multiple add_attributes calls work
- All attributes appear in output

---

### 6.5 Nested Traces
**Objective**: Demonstrate parent-child span relationships

**Example Code**:
```python
def nested_traces_example():
    """Create nested traces"""
    # Setup (same as above)
    
    with get_trace("parent_operation") as parent_span:
        parent_span.add_event("parent_started")
        
        with get_trace("child_operation_1") as child_span:
            child_span.add_event("child_1_work")
            import time
            time.sleep(0.05)
        
        with get_trace("child_operation_2") as child_span:
            child_span.add_event("child_2_work")
            time.sleep(0.05)
        
        parent_span.add_event("parent_completed")
    
    return True
```

**Validation**:
- Parent-child relationships are preserved
- Nested spans have correct timing
- All spans appear in output

---

### 6.6 Trace Propagation
**Objective**: Demonstrate trace context propagation

**Example Code**:
```python
def trace_propagation_example():
    """Propagate trace context across functions"""
    # Setup (same as above)
    
    carrier = {}
    
    # Start trace and inject context
    with get_trace("service_a_request", carrier=carrier) as span:
        span.add_event("service_a_processing")
        import time
        time.sleep(0.05)
    
    # Continue trace in another context
    with get_trace("service_b_request", carrier=carrier) as span:
        span.add_event("service_b_processing")
        time.sleep(0.05)
    
    return True
```

**Validation**:
- Trace context is propagated
- Spans share same trace ID
- Carrier contains trace context

---

## 7. Advanced Scenarios

### 7.1 Multi-Signal Coordination
**Objective**: Demonstrate logs, metrics, and traces together

**Example Code**:
```python
def multi_signal_example():
    """Use all signal types together"""
    # Setup with all signals
    config = Configuration(default_endpoint='http://localhost:4318')
    config.set_console_exporter(use_console=True)
    attrs = ResourceAttributes("hello-world-service", "1.0.0")
    initialize_telemetry(config, attrs, signal_types=['logging', 'metrics', 'tracing'])
    
    # Setup logger
    import logging
    logger = logging.getLogger(__name__)
    logger.addHandler(get_telemetry_logger_handler())
    
    # Coordinated telemetry
    with get_trace("http_request") as span:
        logger.info("Request started")
        increment_counter("requests_total", by=1)
        
        import time
        start_time = time.time()
        time.sleep(0.1)  # Simulate work
        duration = time.time() - start_time
        
        record_histogram("request_duration_seconds", value=duration)
        logger.info("Request completed")
        span.add_event("request_finished")
    
    return True
```

**Validation**:
- All signal types work together
- Telemetry is correlated
- Session ID ties data together

---

### 7.2 Error Handling Pattern
**Objective**: Demonstrate comprehensive error handling

**Example Code**:
```python
def error_handling_example():
    """Demonstrate error handling across signals"""
    # Setup (same as above)
    
    import logging
    logger = logging.getLogger(__name__)
    logger.addHandler(get_telemetry_logger_handler())
    
    with get_trace("error_prone_operation") as span:
        try:
            logger.info("Starting risky operation")
            increment_counter("operations_attempted", by=1)
            
            # Simulate error
            raise RuntimeError("Unexpected error occurred")
            
        except Exception as e:
            # Record error in all signals
            logger.error(f"Operation failed: {e}")
            increment_counter("operations_failed", by=1)
            span.add_exception(e)
            span.set_error_status("Operation failed due to error")
    
    return True
```

**Validation**:
- Errors are captured in all signals
- Telemetry shows error state
- Application continues running

---

### 7.3 Performance Monitoring
**Objective**: Demonstrate performance tracking pattern

**Example Code**:
```python
def performance_monitoring_example():
    """Monitor performance with telemetry"""
    # Setup (same as above)
    
    import time
    
    with get_trace("performance_test") as span:
        # Track operation count
        operations = 100
        increment_counter("operations_total", by=operations)
        
        # Track timing
        start = time.time()
        for i in range(operations):
            # Simulate work
            time.sleep(0.001)
        duration = time.time() - start
        
        # Record performance metrics
        record_histogram("operation_duration_seconds", value=duration)
        record_histogram("operations_per_second", value=operations/duration)
        
        span.add_attributes({
            "operations_count": operations,
            "total_duration": duration,
            "ops_per_second": operations/duration
        })
    
    return True
```

**Validation**:
- Performance metrics are captured
- Timing is accurate
- Metrics show performance characteristics

---

## Test Execution Strategy

### Running Individual Scenarios
```bash
# Run specific example
python -m src.metrics_examples

# Run specific test
pytest tests/test_metrics.py::test_counter_increment
```

### Running All Scenarios
```bash
# Run all examples
python run_examples.py

# Run all tests
pytest tests/
```

### Validation Criteria

Each scenario must:
1. ✅ Execute without errors
2. ✅ Produce expected console output
3. ✅ Pass automated test validation
4. ✅ Demonstrate documented SDK behavior
5. ✅ Be simple and understandable

### Output Verification

For each scenario, verify:
- Console exporter shows telemetry data
- Data structure matches OpenTelemetry format
- Attributes are present and correct
- Timestamps are reasonable
- No error messages (unless testing errors)

---

## Coverage Matrix

| SDK Method | Scenario | Test File |
|------------|----------|-----------|
| `Configuration()` | 1.1 | test_config.py |
| `set_console_exporter()` | 1.2 | test_config.py |
| `set_*_endpoint()` | 1.3 | test_config.py |
| `set_*_export_interval_ms()` | 1.4 | test_config.py |
| `set_tracing_session_entropy()` | 1.5 | test_config.py |
| `set_logging_level()` | 1.6 | test_config.py |
| `ResourceAttributes()` | 2.1 | test_attributes.py |
| `set_attributes()` | 2.2, 2.3 | test_attributes.py |
| `initialize_telemetry()` | 3.1, 3.2, 3.3 | test_initialization.py |
| `get_telemetry_logger_handler()` | 4.1, 4.2 | test_logging.py |
| `increment_counter()` | 5.1, 5.4 | test_metrics.py |
| `decrement_counter()` | 5.2, 5.4 | test_metrics.py |
| `record_histogram()` | 5.3, 5.4 | test_metrics.py |
| `get_trace()` | 6.1-6.6 | test_tracing.py |
| `span.add_event()` | 6.2 | test_tracing.py |
| `span.add_exception()` | 6.3 | test_tracing.py |
| `span.set_error_status()` | 6.3 | test_tracing.py |
| `span.add_attributes()` | 6.4 | test_tracing.py |
| Multi-signal | 7.1, 7.2, 7.3 | test_advanced.py |

**Total Coverage**: 100% of public SDK methods
