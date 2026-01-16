# E2E QA Project - Architecture Design

## Project Structure

```
tests/e2e_qa/
├── _docs/                          # Design and specification documents
│   ├── 01_project_overview.md
│   ├── 02_architecture_design.md
│   ├── 03_implementation_plan.md
│   └── 04_test_scenarios.md
│
├── src/                            # Source code for examples
│   ├── __init__.py
│   ├── config_examples.py          # Configuration demonstrations
│   ├── attributes_examples.py      # ResourceAttributes demonstrations
│   ├── initialization_examples.py  # Initialization demonstrations
│   ├── logging_examples.py         # Logging signal demonstrations
│   ├── metrics_examples.py         # Metrics signal demonstrations
│   ├── tracing_examples.py         # Tracing signal demonstrations
│   └── advanced_examples.py        # Advanced usage patterns
│
├── tests/                          # Automated validation tests
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_attributes.py
│   ├── test_initialization.py
│   ├── test_logging.py
│   ├── test_metrics.py
│   ├── test_tracing.py
│   └── test_advanced.py
│
├── requirements.txt                # Project dependencies
├── pyproject.toml                  # Project configuration
├── README.md                       # Project documentation
└── run_examples.py                 # Main entry point to run all examples

```

## Design Principles

### 1. Separation of Concerns
- **Configuration Examples**: Isolated in `config_examples.py`
- **Signal Examples**: Each signal type (logging, metrics, tracing) in separate files
- **Test Validation**: Separate test files mirror example files

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
```bash
# Install SDK as external package (conda recommended)
conda install anaconda-opentelemetry

# Or using pip
pip install anaconda-opentelemetry
```

```python
# Import as external consumer
from anaconda.opentelemetry import (
    Configuration,
    ResourceAttributes,
    initialize_telemetry,
    record_histogram,
    increment_counter,
    decrement_counter,
    get_trace,
    get_telemetry_logger_handler
)
```

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

## Test Strategy

### Unit-Style Validation Tests
Each test file validates corresponding examples:

```python
def test_basic_configuration():
    """Validate basic configuration example works"""
    result = config_examples.basic_configuration()
    assert result is not None
    assert isinstance(result, Configuration)

def test_increment_counter():
    """Validate counter increment works"""
    result = metrics_examples.increment_counter_example()
    assert result is True
```

### Integration Validation
- Verify all examples run without errors
- Validate output contains expected telemetry data
- Check console exporter output for correctness

### Coverage Goals
- 100% of SDK public methods demonstrated
- All common usage patterns covered
- Error scenarios documented

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

### Core Dependencies

**Primary Installation Method (Recommended)**:
```bash
# Using conda
conda install anaconda-opentelemetry
```

**Alternative Installation Method**:
```bash
# Using pip
pip install anaconda-opentelemetry>=1.0.0
```

### Development Dependencies
```
pytest>=7.0.0                   # Test framework
pytest-cov>=4.0.0              # Coverage reporting
```

**Installation**:
```bash
# Install test dependencies (after SDK is installed)
pip install pytest pytest-cov
```

### Optional Dependencies
```
# None - keeping it minimal
```

### Environment Setup

**Recommended Approach**:
```bash
# Create conda environment with SDK
conda create -n e2e-qa-test anaconda-opentelemetry python=3.10

# Activate environment
conda activate e2e-qa-test

# Install test dependencies
pip install pytest pytest-cov
```

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

### Validation Feedback
- Clear success/failure indicators
- Descriptive error messages
- Suggestions for common issues

## Extensibility

### Adding New Examples
1. Create function in appropriate module
2. Follow naming convention: `{feature}_example()`
3. Add docstring with description
4. Include in main runner
5. Create corresponding test

### Adding New Test Scenarios
1. Identify SDK feature to test
2. Create example demonstrating feature
3. Write validation test
4. Document expected behavior
