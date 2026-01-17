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

## Critical Backend Data Requirements

### ⚠️ Console Exporter vs Remote Backend (Mutually Exclusive)

**The console exporter and remote backend exporter are MUTUALLY EXCLUSIVE!**

When you set `config.set_console_exporter(use_console=True)`:
- ✅ Data is printed to console (for debugging)
- ❌ Data is **NOT sent to remote backend**

When you set `config.set_console_exporter(use_console=False)`:
- ❌ Data is **NOT printed to console**
- ✅ Data **IS sent to remote backend**

**For Backend Validation**: Set `OTEL_CONSOLE_EXPORTER=false` in `.env`

```python
# ❌ WRONG - Data only goes to console, NOT backend
config.set_console_exporter(use_console=True)
initialize_telemetry(config, attrs)
increment_counter("test_metric", by=1)
# Data printed to console but NEVER reaches backend!

# ✅ CORRECT - Data goes to backend
config.set_console_exporter(use_console=False)  # or don't call it at all
initialize_telemetry(config, attrs)
increment_counter("test_metric", by=1)
flush_telemetry()  # Ensure it's sent
# Data reaches backend!
```

### ⚠️ Flush Requirement for Short-Lived Programs

OpenTelemetry uses **batching** to optimize network usage:
- Metrics, logs, and traces are collected in memory
- They are exported in batches at regular intervals (default: 30-60 seconds)
- **Short-lived programs exit before the batch export happens**
- Result: Data never reaches the backend

**Solution**: Force flush before exit

```python
def flush_telemetry():
    """
    Force flush all telemetry data to ensure it's sent to the backend.
    CRITICAL for short-lived programs!
    """
    from opentelemetry import metrics, trace
    from anaconda.opentelemetry.signals import _AnacondaLogger
    
    try:
        # Flush metrics
        meter_provider = metrics.get_meter_provider()
        if hasattr(meter_provider, 'force_flush'):
            meter_provider.force_flush(timeout_millis=5000)
        
        # Flush traces
        tracer_provider = trace.get_tracer_provider()
        if hasattr(tracer_provider, 'force_flush'):
            tracer_provider.force_flush(timeout_millis=5000)
        
        # Flush logs
        if _AnacondaLogger._instance:
            logger_instance = _AnacondaLogger._instance
            if hasattr(logger_instance, '_provider') and logger_instance._provider:
                logger_instance._provider.force_flush(timeout_millis=5000)
                
        print("✓ Telemetry flushed successfully")
    except Exception as e:
        print(f"⚠️  Warning: Error during flush: {e}")
```

**When to Flush**:

| Scenario | Flush Required? | Reason |
|----------|----------------|---------|
| Script/CLI tool | ✅ YES | Exits quickly, batch not exported |
| Test suite | ✅ YES | Tests finish in seconds |
| Lambda function | ✅ YES | Function terminates after execution |
| Web server | ❌ NO | Runs indefinitely, auto-exports |
| Background daemon | ❌ NO | Long-running, auto-exports |
| E2E Examples | ✅ YES | Script that exits after tests |

**Best Practice**: Use try-finally for guaranteed flush

```python
def main():
    initialize_telemetry(config, attrs)
    
    try:
        # Your code here
        increment_counter("operations", by=1)
    finally:
        # Guaranteed to flush even if error occurs
        flush_telemetry()
```

---

## Process Isolation Architecture

### ⚠️ OpenTelemetry Single Initialization Limitation

**OpenTelemetry only allows ONE initialization per process!**

If you try to call `initialize_telemetry()` multiple times in the same Python process:
- ✅ **First call**: Succeeds, sets service name and configuration
- ❌ **Subsequent calls**: Silently ignored (returns immediately)
- 🐛 **Result**: All metrics are sent under the first service name

#### The Problem

From `signals.py`:

```python
def initialize_telemetry(config, attributes, signal_types):
    global __ANACONDA_TELEMETRY_INITIALIZED
    
    if __ANACONDA_TELEMETRY_INITIALIZED is True:
        return  # ⚠️ Silently returns - no error, no warning!
```

This is a **global flag** that prevents re-initialization. Once set to `True`, all subsequent calls are no-ops.

#### Example of the Bug

```python
# ❌ WRONG - All metrics will use "service-a"
initialize_telemetry(config, ResourceAttributes(service_name="service-a"))
increment_counter("metric_a", by=1)

initialize_telemetry(config, ResourceAttributes(service_name="service-b"))  # IGNORED!
increment_counter("metric_b", by=1)  # Still uses "service-a"!

# Backend will show:
# - service-a: metric_a, metric_b  ❌ Wrong!
```

#### Impact on Multiple Initializations

If multiple `initialize_telemetry()` calls occur in sequence within the same process:

```python
# First initialization - succeeds
initialize_telemetry(config, ResourceAttributes(service_name="example-01-all-signals"))
increment_counter("example_01_initialization_test", by=1)

# Second initialization - silently ignored
initialize_telemetry(config, ResourceAttributes(service_name="example-02-metrics-only"))
increment_counter("example_02_metrics_test", by=1)

# Third initialization - silently ignored
initialize_telemetry(config, ResourceAttributes(service_name="example-03-default"))
increment_counter("example_03_default_test", by=1)
```

**Result**: All 3 metrics would be sent under `service_name="example-01-all-signals"` because only the first initialization takes effect!

### Solution: Separate Processes for Each Example

**Design**: Individual scripts + process runner

```
examples/
├── 01_all_signals.py          # Separate process
├── 02_metrics_only.py          # Separate process
├── 03_default.py               # Separate process
├── 04_selective.py             # Separate process
├── 05_complete.py              # Separate process
└── 06_env_based.py             # Separate process

run_initialization_examples.py  # Runs each as subprocess
```

#### How It Works

```python
# run_initialization_examples.py
for example_script in EXAMPLES:
    subprocess.run([sys.executable, example_script])  # New process!
```

Each subprocess:
1. Starts with fresh Python interpreter
2. Initializes telemetry with its own service name
3. Sends its metric
4. Flushes and exits
5. Next subprocess starts clean

**Result**: Each metric gets its own service name! ✅

### Why Not Fix in SDK?

#### Option 1: Allow Re-initialization (Breaking Change)

**Problems**:
- Breaking change for existing users
- Could cause resource leaks (multiple providers)
- Unclear semantics (what happens to existing metrics?)

#### Option 2: Warn on Re-initialization

```python
def initialize_telemetry(config, attributes, signal_types):
    if __ANACONDA_TELEMETRY_INITIALIZED is True:
        logging.warning("Telemetry already initialized - ignoring call")
        return
```

**Better**, but still doesn't solve the E2E test issue.

#### Option 3: Separate Processes (Current Solution)

**Pros**:
- ✅ No SDK changes needed
- ✅ Clean separation of concerns
- ✅ Matches real-world usage (one service = one process)
- ✅ Each test is truly independent

**Cons**:
- ❌ Slightly more complex test setup
- ❌ Can't share state between examples (but this is actually good!)

**Decision**: Use separate processes - it's the most realistic and robust approach.

### Lessons Learned

1. **OpenTelemetry is designed for long-lived services**, not test suites
2. **Global state in SDKs can cause subtle bugs** in test environments
3. **Process isolation is the safest way** to test initialization
4. **Silent failures are dangerous** - SDK should warn on re-init attempts

### Script Architecture

```
run_all_examples.py
├── Imports and runs: 01_config_examples.py (same process)
├── Imports and runs: 02_attributes_examples.py (same process)
└── Subprocess calls: run_initialization_examples.py
    ├── Subprocess: examples/01_all_signals.py
    ├── Subprocess: examples/02_metrics_only.py
    ├── Subprocess: examples/03_default.py
    ├── Subprocess: examples/04_selective.py
    ├── Subprocess: examples/05_complete.py
    └── Subprocess: examples/06_env_based.py
```

Each initialization example gets a **fresh Python interpreter** with clean global state, ensuring proper service name isolation.


## Extensibility

### Adding New Examples
1. Create function in appropriate module
2. Follow naming convention: `{feature}_example()`
3. Add docstring with description
4. Include in main runner (`run_all_examples.py`)
5. Document expected behavior and output
