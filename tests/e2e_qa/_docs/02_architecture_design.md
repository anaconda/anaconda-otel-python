# E2E QA Project - Architecture Design

## Architecture Overview

This document describes the technical architecture and design principles.

## Design Principles

### 1. Separation of Concerns
- **Configuration Examples**: Isolated in `config_examples.py`
- **Signal Examples**: Each signal type (logging, metrics, tracing) in separate files
- **Clear Organization**: Each module focuses on a specific SDK feature area

### 2. Progressive Complexity
Each example file follows this pattern:
1. **Basic Example**: Minimal setup, single method call
2. **Intermediate Example**: Multiple related method calls
3. **Advanced Example**: Real-world scenario with multiple features

### 3. Self-Contained Examples
Each example function:
- Has clear docstring explaining what it demonstrates
- Includes all necessary setup
- Produces visible output (console or return value)
- Handles errors gracefully
- Can be run independently

### 4. External Package Integration
Install SDK via conda and import as external package.

## Module Breakdown

### 1. Configuration Examples (`config_examples.py`)
Demonstrates all Configuration class methods:
- Basic endpoint configuration
- Signal-specific endpoints (logging, tracing, metrics)
- Console exporter setup
- Export intervals
- Session entropy
- TLS/authentication settings

### 2. Attributes Examples (`attributes_examples.py`)
Demonstrates ResourceAttributes:
- Basic attribute setup
- Setting common attributes (os_type, hostname, etc.)
- Dynamic attributes via `set_attributes()`
- Environment-specific attributes

### 3. Initialization Examples (`initialization_examples.py`)
Demonstrates initialization patterns:
- Basic initialization with all signals
- Selective signal initialization
- Multiple initialization patterns
- Error handling

### 4. Logging Examples (`logging_examples.py`)
Demonstrates logging signal:
- Getting logger handler
- Adding handler to logger
- Different log levels
- Structured logging with attributes
- Integration with Python logging

### 5. Metrics Examples (`metrics_examples.py`)
Demonstrates metrics signal:
- `increment_counter()` with attributes
- `decrement_counter()` for up/down counters
- `record_histogram()` for distributions
- Different metric types
- Metric naming conventions

### 6. Tracing Examples (`tracing_examples.py`)
Demonstrates tracing signal:
- Basic trace context manager
- Adding events to spans
- Adding exceptions to spans
- Setting error status
- Adding attributes to spans
- Trace propagation with carrier

### 7. Advanced Examples (`advanced_examples.py`)
Demonstrates complex scenarios:
- Multi-signal coordination
- Distributed tracing across functions
- Error handling and recovery
- Performance monitoring patterns
- Real-world application simulation

## Execution Flow

### Main Entry Point (`run_examples.py`)
```python
def main():
    """Run all examples in sequence"""
    print("=== Configuration Examples ===")
    run_config_examples()
    
    print("\n=== Attributes Examples ===")
    run_attributes_examples()
    
    print("\n=== Initialization Examples ===")
    run_initialization_examples()
    
    print("\n=== Logging Examples ===")
    run_logging_examples()
    
    print("\n=== Metrics Examples ===")
    run_metrics_examples()
    
    print("\n=== Tracing Examples ===")
    run_tracing_examples()
    
    print("\n=== Advanced Examples ===")
    run_advanced_examples()
```

## Output Strategy

### Console Output
All examples use console exporter for immediate visibility:
```python
config = Configuration(default_endpoint='http://localhost:4318')
config.set_console_exporter(use_console=True)
```

### Structured Output
Each example produces:
1. **Description**: What the example demonstrates
2. **Code Execution**: The actual SDK calls
3. **Telemetry Output**: Console exporter output
4. **Validation**: Success/failure indication

Example output format:
```
--- Example: Basic Counter Increment ---
Description: Demonstrates incrementing a counter with attributes
Executing: increment_counter("user_login", by=1, attributes={"user_id": "123"})

[Console Exporter Output]
{
  "scopeMetrics": [...],
  "name": "user_login",
  ...
}

✓ Example completed successfully
```

## Dependencies

**Core**: `anaconda-opentelemetry` (installed via conda)
**Optional**: None - minimal hello-world setup

## Error Handling Strategy

### Graceful Degradation
```python
def example_with_error_handling():
    """Example with proper error handling"""
    try:
        config = Configuration(default_endpoint='http://localhost:4318')
        attrs = ResourceAttributes("example-service", "1.0.0")
        initialize_telemetry(config, attrs)
        return True
    except Exception as e:
        print(f"❌ Example failed: {e}")
        return False
```

### User Feedback
- Clear success/failure indicators in console output
- Descriptive error messages
- Suggestions for common issues

## Extensibility

### Adding New Examples
1. Create function in appropriate module
2. Follow naming convention: `{feature}_example()`
3. Add docstring with description
4. Include in main runner (`run_all_examples.py`)
5. Document expected behavior and output
