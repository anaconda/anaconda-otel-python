# Hello-World Examples - Anaconda OpenTelemetry Python SDK

## Overview

Simple, runnable examples demonstrating all methods of the `anaconda-opentelemetry` Python SDK. Each example is self-contained and can be executed independently.

## Project Structure

```
tests/e2e_qa/
├── _docs/                          # Design specifications
│   ├── 00_summary.md              # Project summary
│   ├── 01_requirements.md          # Requirements (authoritative)
│   ├── 02_architecture_design.md   # Technical architecture
│   ├── 03_implementation_plan.md   # Development phases
│   ├── 04_test_scenarios.md        # Example scenarios
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

- **Python 3.9+** (3.10 recommended)
- **conda** package manager

### Installation

```bash
# Create environment from file
cd tests/e2e_qa
conda env create -f environment.yml.template
conda activate e2e-qa-test
```

Or create manually:
```bash
conda create -n e2e-qa-test anaconda-opentelemetry python=3.10
conda activate e2e-qa-test
```

### Running Examples

```bash
# Run all examples
python run_all_examples.py

# Run specific example
python examples/05_metrics_examples.py
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

See `_docs/` directory for:
- Architecture and design
- Implementation plan
- Detailed scenarios
- Documentation index

## Development

To add new examples:
1. Create function in appropriate module
2. Make it runnable with `if __name__ == "__main__"`
3. Update documentation

## SDK Method Coverage

Demonstrates all public SDK methods (23 total):
- **Configuration** (11): Endpoints, console exporter, intervals, logging level
- **Attributes** (2): ResourceAttributes, set_attributes
- **Initialization** (1): initialize_telemetry
- **Logging** (1): get_telemetry_logger_handler
- **Metrics** (3): increment_counter, decrement_counter, record_histogram
- **Tracing** (5): get_trace, span events/exceptions/attributes

## Use Cases

- **New Users**: Learn SDK through simple examples
- **Integration Engineers**: Copy working patterns into projects
- **SDK Developers**: Verify API usability
- **Documentation**: Living, executable code examples

## Troubleshooting

**Module not found**:
```bash
conda activate e2e-qa-test
conda install anaconda-opentelemetry
```

**No output**: Ensure `config.set_console_exporter(use_console=True)`

**Conda issues**: See `_docs/07_conda_setup.md`

## Contributing

1. Review design documents in `_docs/`
2. Follow existing code style
3. Update documentation
4. Submit pull request
