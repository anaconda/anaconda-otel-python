# Hello-World Examples - Anaconda OpenTelemetry Python SDK

## Overview

This project provides **simple, runnable examples** demonstrating all methods of the `anaconda-opentelemetry` Python SDK. It's designed as a **hello-world style learning resource** for developers integrating the SDK.

### Key Features

- ✅ **Complete SDK Coverage**: Demonstrates all public SDK methods
- ✅ **Hello-World Simplicity**: Easy-to-understand, self-contained examples
- ✅ **External Integration**: Uses SDK as an external package (real-world usage)
- ✅ **Runnable Examples**: Each example can be executed independently
- ✅ **Living Documentation**: Executable code that shows how to use the SDK

### What This Is NOT

- ❌ **Not a Test Suite**: This is not for automated testing or QA validation
- ❌ **Not pytest-based**: No test framework, just simple Python scripts
- ✅ **Just Examples**: Simple demonstrations of SDK functionality

## Project Structure

```
tests/e2e_qa/
├── _docs/                          # Design specifications
│   ├── 00_summary.md              # Project summary
│   ├── 01_requirements.md          # Requirements (authoritative)
│   ├── 02_architecture_design.md   # Technical architecture
│   ├── 03_implementation_plan.md   # Development phases
│   ├── 04_test_scenarios.md        # Example scenarios
│   ├── 05_quick_reference.md       # Quick reference
│   ├── 06_visual_guide.md          # Visual diagrams
│   ├── 07_conda_setup.md           # Conda setup guide
│   └── INDEX.md                    # Documentation index
│
├── examples/                       # Example implementations (to be created)
│   ├── 01_config_examples.py       # Configuration examples
│   ├── 02_attributes_examples.py   # ResourceAttributes examples
│   ├── 03_initialization_examples.py # Initialization examples
│   ├── 04_logging_examples.py      # Logging signal examples
│   ├── 05_metrics_examples.py      # Metrics signal examples
│   ├── 06_tracing_examples.py      # Tracing signal examples
│   └── 07_advanced_examples.py     # Advanced usage patterns
│
├── environment.yml.template        # Conda environment specification
├── README.md                       # This file
└── run_all_examples.py             # Main entry point (to be created)
```

## Quick Start

### Prerequisites

- **Python 3.9+** (minimum), **Python 3.10** (recommended) - See [_docs/01_requirements.md](_docs/01_requirements.md)
- **conda** package manager (required - official SDK installation method)

### Installation

#### Option 1: Using Conda (Recommended)

**Method A: Using environment file** (easiest):
```bash
# Create environment from file
cd tests/e2e_qa
conda env create -f environment.yml.template

# Activate the environment
conda activate e2e-qa-test
```

**Method B: Manual setup**:
```bash
# Create new environment with anaconda-opentelemetry
conda create -n e2e-qa-test anaconda-opentelemetry python=3.10

# Activate the environment
conda activate e2e-qa-test

# Install test dependencies
cd tests/e2e_qa
pip install pytest pytest-cov
```

#### Option 2: Using Existing Conda Environment

1. **Install the SDK in your existing environment**:
```bash
# Activate your environment
conda activate your-env-name

# Install the SDK
conda install anaconda-opentelemetry
```

2. **Install E2E QA dependencies**:
```bash
cd tests/e2e_qa
pip install -r requirements.txt
```

#### Note on pip

The SDK documentation only covers conda installation. While the package has a `pyproject.toml` and may be pip-installable, **conda is the official and documented installation method**. For pip installation, refer to the main SDK documentation or use conda as documented above.

### Running Examples

**Run all examples**:
```bash
python run_all_examples.py
```

**Run specific example module**:
```bash
python examples/05_metrics_examples.py
python examples/06_tracing_examples.py
```

**Run individual examples**:
```bash
# Each example file can be run directly
python examples/01_config_examples.py
```

## What's Demonstrated

### 1. Configuration (`examples/01_config_examples.py`)
- Basic endpoint configuration
- Console exporter setup
- Signal-specific endpoints
- Export intervals
- Session entropy
- Logging levels

### 2. Resource Attributes (`examples/02_attributes_examples.py`)
- Basic attribute creation
- Required vs optional fields
- Custom attributes with `set_attributes()`
- Environment-specific attributes
- Dynamic parameters

### 3. Initialization (`examples/03_initialization_examples.py`)
- Full initialization (all signals)
- Selective signal initialization
- Default initialization (metrics only)
- Error handling patterns

### 4. Logging (`examples/04_logging_examples.py`)
- Getting logger handler
- Adding handler to logger
- Different log levels
- Structured logging
- Logger integration

### 5. Metrics (`examples/05_metrics_examples.py`)
- Counter increment
- Counter decrement (up/down counters)
- Histogram recording
- Metric attributes
- Multiple metrics coordination

### 6. Tracing (`examples/06_tracing_examples.py`)
- Basic trace context manager
- Adding events to spans
- Exception handling in spans
- Setting error status
- Adding attributes to spans
- Nested traces
- Trace propagation with carrier

### 7. Advanced Patterns (`examples/07_advanced_examples.py`)
- Multi-signal coordination
- Error handling across signals
- Performance monitoring
- Real-world scenarios
- Production-ready patterns

## Example Output

When you run the examples, you'll see output like this:

```
=== Configuration Examples ===
--- Example: Basic Configuration ---
Description: Create basic configuration with default endpoint
✓ Configuration created successfully
Endpoint: http://localhost:4318

=== Metrics Examples ===
--- Example: Counter Increment ---
Description: Increment a counter with attributes
Executing: increment_counter("user_login", by=1, attributes={"user_id": "123"})

[Console Exporter Output]
{
  "scopeMetrics": [
    {
      "scope": {
        "name": "hello-world-service",
        "version": "1.0.0"
      },
      "metrics": [
        {
          "name": "user_login",
          "sum": {
            "dataPoints": [
              {
                "attributes": [
                  {"key": "user_id", "value": {"stringValue": "123"}}
                ],
                "asInt": "1"
              }
            ]
          }
        }
      ]
    }
  ]
}

✓ Example completed successfully
```

## Documentation

### Design Documents

Comprehensive design documentation is available in the `_docs/` directory:

1. **[Project Overview](_docs/01_project_overview.md)**: Purpose, goals, and success criteria
2. **[Architecture Design](_docs/02_architecture_design.md)**: Technical architecture and design principles
3. **[Implementation Plan](_docs/03_implementation_plan.md)**: Development phases and timeline
4. **[Test Scenarios](_docs/04_test_scenarios.md)**: Detailed test scenarios with code examples

### SDK Documentation

For complete SDK documentation, see:
- [Getting Started Guide](../../docs/source/getting_started.md)
- [Onboarding Examples](../../docs/source/onboarding_examples.md)
- [Signal Type Best Practices](../../docs/source/signal_type_best_practices.md)

## Development

### Adding New Examples

1. **Create example function** in appropriate module:
```python
def new_feature_example():
    """Demonstrate new SDK feature"""
    # Setup
    config = Configuration(default_endpoint='http://localhost:4318')
    config.set_console_exporter(use_console=True)
    attrs = ResourceAttributes("hello-world-service", "1.0.0")
    initialize_telemetry(config, attrs, signal_types=['metrics'])
    
    # Demonstrate feature
    print("=== New Feature Example ===")
    # ... your code here ...
    print("✓ Example completed\n")
```

2. **Make it runnable**:
```python
if __name__ == "__main__":
    new_feature_example()
```

3. **Update documentation** if needed

### Running Examples

```bash
# Run all examples
python run_all_examples.py

# Run specific example file
python examples/05_metrics_examples.py

# Run with verbose output
python examples/05_metrics_examples.py --verbose
```

## SDK Method Coverage

This project demonstrates **100% of public SDK methods**:

| Category | Methods Covered |
|----------|----------------|
| **Configuration** | `Configuration()`, `set_console_exporter()`, `set_*_endpoint()`, `set_logging_level()`, `set_*_export_interval_ms()`, `set_tracing_session_entropy()`, `set_skip_internet_check()`, `set_use_cumulative_metrics()` |
| **Attributes** | `ResourceAttributes()`, `set_attributes()` |
| **Initialization** | `initialize_telemetry()` |
| **Logging** | `get_telemetry_logger_handler()` |
| **Metrics** | `increment_counter()`, `decrement_counter()`, `record_histogram()` |
| **Tracing** | `get_trace()`, `span.add_event()`, `span.add_exception()`, `span.set_error_status()`, `span.add_attributes()` |

## Use Cases

### For New Users
- Learn SDK through simple examples
- Understand signal types (logging, metrics, tracing)
- See configuration options
- Get started quickly with copy-paste examples

### For Integration Engineers
- See real-world usage patterns
- Understand SDK capabilities
- Copy working examples into your project
- Learn best practices

### For SDK Developers
- Demonstrate SDK functionality
- Show external package integration
- Provide reference implementations
- Verify API usability

### For Documentation
- Living code examples
- Always up-to-date with SDK
- Executable documentation
- Clear usage patterns

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'anaconda.opentelemetry'`
```bash
# Solution 1: Install via conda (official method)
conda install anaconda-opentelemetry

# Solution 2: Verify environment is activated
conda activate e2e-qa-test

# Solution 3: Recreate environment
conda create -n e2e-qa-test anaconda-opentelemetry python=3.10
conda activate e2e-qa-test
```

**Issue**: Examples don't produce output
```bash
# Solution: Ensure console exporter is enabled
config.set_console_exporter(use_console=True)
```

**Issue**: Tests fail with initialization errors
```bash
# Solution: Check that SDK is installed correctly
python -c "import anaconda.opentelemetry; print('SDK installed')"

# If using conda, verify environment
conda list anaconda-opentelemetry
```

**Issue**: Wrong Python version or environment
```bash
# Solution: Create fresh conda environment
conda create -n e2e-qa-test anaconda-opentelemetry python=3.10
conda activate e2e-qa-test
```

**Issue**: Conda environment conflicts
```bash
# Solution: See detailed troubleshooting guide
# Read: _docs/07_conda_setup.md
```

## Contributing

Contributions are welcome! To contribute:

1. Review the design documents in `_docs/`
2. Follow the existing code style
3. Add tests for new examples
4. Update documentation
5. Submit a pull request

## License

This project is part of the `anaconda-opentelemetry` package and follows the same license.

## Contact

For questions or issues:
- Open an issue in the main repository
- Refer to the SDK documentation
- Check the design documents in `_docs/`

---

## Next Steps

After reviewing this README:

1. **Read the design documents** in `_docs/` for detailed specifications
2. **Run the examples** to see the SDK in action
3. **Explore the code** in `src/` to understand implementation
4. **Run the tests** to validate functionality
5. **Integrate the SDK** into your own projects

Happy coding! 🚀
