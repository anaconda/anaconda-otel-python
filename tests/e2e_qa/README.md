# Hello-World Examples - Anaconda OpenTelemetry Python SDK

## Overview

Simple, runnable examples demonstrating all methods of the `anaconda-opentelemetry` Python SDK. Each example is self-contained and can be executed independently.

### Example Philosophy: Progressive Learning

This collection uses a **progressive disclosure approach** with two complementary example types:

1. **Atomic Examples** - Focus on one concept at a time
   - Clear, minimal code showing a single pattern
   - Easy to understand and copy-paste
   - Perfect for learning and quick reference
   - Helps isolate issues during troubleshooting

2. **Complex Examples** - Show real-world integration
   - Demonstrate multiple features working together
   - Production-ready configurations
   - Show best practices and advanced patterns
   - Serve as comprehensive templates

**Why both?** Different users have different needs:
- **New users** benefit from atomic examples to learn step-by-step
- **Experienced users** can copy atomic examples for specific use cases
- **Production deployments** use complex examples as starting templates
- **Troubleshooting** is easier with atomic examples (test one thing at a time)

This dual approach ensures the SDK is accessible to beginners while providing depth for advanced use cases.

## Project Structure

```
tests/e2e_qa/
│
├── examples/                       # Example implementations
│   ├── 01_config_examples.py       # Configuration examples
│   ├── 02_attributes_examples.py   # ResourceAttributes examples
│   ├── 01_all_signals.py           # Init: All signals
│   ├── 02_metrics_only.py          # Init: Metrics only
│   ├── 03_default.py               # Init: Default config
│   ├── 04_selective.py             # Init: Selective signals
│   ├── 05_complete.py              # Init: Complete setup
│   ├── 06_env_based.py             # Init: Environment-based
│   └── 07_flush_test.py            # Init: Explicit flush test
│
├── .env                            # Environment configuration (create from env.example)
├── env.example                     # Example environment configuration
├── environment.yml                 # Conda environment specification
├── README.md                       # This file
└── run_all_examples.py             # Main entry point
```

## Quick Start

### Prerequisites

- **Conda** package manager installed
- **Python 3.9+** (3.10 recommended)
- **Git** (to clone the repository)
- **OpenTelemetry collector endpoint** (provided by your organization)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd anaconda-otel-python/tests/e2e_qa
   ```

2. **Create and activate conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate e2e-qa-examples
   ```

3. **Install SDK in development mode**
   ```bash
   cd ../..  # Go to repo root
   pip install -e .
   cd tests/e2e_qa
   ```

4. **Configure environment**
   
   Create a `.env` file from the example:
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and set the required variables:
   ```bash
   # Required: Set your environment name
   OTEL_ENVIRONMENT=your_env_name
   
   # Required: Set your OpenTelemetry collector endpoint URL
   OTEL_ENDPOINT=https://your-collector-endpoint.com
   
   # Optional: Enable console output for local debugging
   OTEL_CONSOLE_EXPORTER=false  # Set to true for console-only output
   
   # Optional: API key if your endpoint requires authentication
   # OTEL_API_KEY=your-api-key-here
   ```
   
   **Important Notes**:
   - ⚠️ When `OTEL_CONSOLE_EXPORTER=true`, data is printed to console only (not sent to backend)
   - ⚠️ When `OTEL_CONSOLE_EXPORTER=false`, data is sent to the backend endpoint
   - Contact your organization's telemetry team for endpoint URLs and credentials

5. **Verify installation**
   ```bash
   python -c "from anaconda.opentelemetry import Configuration, ResourceAttributes, initialize_telemetry; print('✓ SDK imported successfully')"
   ```

### Running Examples

All examples should be run from the `tests/e2e_qa/` directory:

```bash
cd tests/e2e_qa
```

#### 🚀 Recommended: Run Individual Examples

**Run from the examples directory**:
```bash
cd examples

# Run any initialization example
python 01_all_signals.py
python 02_metrics_only.py
python 03_default.py
python 04_selective.py
python 05_complete.py
python 06_env_based.py
python 07_flush_test.py

# Run configuration or attributes examples (demonstration only, no backend data)
python 01_config_examples.py
python 02_attributes_examples.py
```

#### Alternative: Run All Examples

**From the e2e_qa directory**:
```bash
# Run all initialization examples (each in separate process)
python run_initialization_examples.py

# Run all logging examples (each in separate process)
python run_logging_examples.py

# Run all metrics examples (each in separate process)
python run_metrics_examples.py

# Or run all example categories (config + attributes + initialization + logging + metrics)
python run_all_examples.py
```

**Note**: Initialization examples run in separate processes to ensure proper OpenTelemetry initialization (only one initialization per process is allowed).


## What's Demonstrated

### 1. Configuration & Attributes
- **`01_config_examples.py`** - Endpoint configuration, console exporter, signal-specific endpoints, export intervals
- **`02_attributes_examples.py`** - Resource attributes, required/optional fields, custom attributes, environment-specific attributes

### 2. Initialization (7 examples via `run_initialization_examples.py`)

Each example runs in a separate process to ensure proper OpenTelemetry initialization.

**Quick Selection:**
- **`03_default.py`** - Simplest setup with SDK defaults
- **`01_all_signals.py`** - All signals (metrics, logs, traces) for full observability
- **`02_metrics_only.py`** - Metrics only for minimal overhead
- **`04_selective.py`** - Specific signal combinations (e.g., metrics + tracing)
- **`05_complete.py`** - Production-ready with all configuration options
- **`06_env_based.py`** - Environment-aware setup (dev/staging/prod)
- **`07_flush_test.py`** - Explicit flush call

### 3. Logging (6 examples via `run_logging_examples.py`)

- **`08_logging_basic.py`** - Basic logging with telemetry handler
- **`09_logging_levels.py`** - All Python logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **`10_logging_structured.py`** - Structured logging with attributes
- **`11_logging_multiple.py`** - Multiple named loggers for different components
- **`12_logging_integration.py`** - Integration with metrics and traces
- **`13_logging_flush.py`** - Explicit flush call

### 4. Metrics (6 examples via `run_metrics_examples.py`)

- **`14_metrics_counters.py`** - Counter metrics for monotonically increasing values
- **`15_metrics_histogram.py`** - Histogram metrics for distributions
- **`16_metrics_updown.py`** - Up/down counters for values that can increase or decrease
- **`17_metrics_attributes.py`** - Multi-dimensional metrics with attributes
- **`18_metrics_patterns.py`** - Real-world metrics patterns and best practices
- **`19_metrics_flush.py`** - Explicit flush call

## Example Output

When you run the examples, you'll see clear output showing:
- SDK method calls being executed
- Configuration details
- Resource attributes
- Success indicators
- Flush confirmation messages

### Verifying Data Delivery

After running examples with `OTEL_CONSOLE_EXPORTER=false`:
1. Wait 1-5 minutes for backend processing
2. Query your telemetry backend for the service names:
   - `example-01-all-signals`
   - `example-02-metrics-only`
   - `example-03-default`
   - `example-04-selective`
   - `example-05-complete`
   - `example-06-env-based`
   - `example-07-flush-test`
3. Each service should have sent at least one metric with value=1

Contact your organization's telemetry team for backend access and query instructions.

## Documentation

See `_docs/` directory for detailed documentation:
- Architecture and design specifications
- Implementation plans and test scenarios
- Visual guides and diagrams
- Complete documentation index

Key document:
- **[INDEX.md](_docs/INDEX.md)** - Complete documentation index

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

### Installation Issues

**`ModuleNotFoundError: No module named 'anaconda'`**
```bash
# Install SDK in development mode from repo root
cd /path/to/anaconda-otel-python
pip install -e .
```

**`ModuleNotFoundError: No module named 'dotenv'`**
```bash
# Recreate the conda environment
conda env create -f environment.yml --force
```

**Conda environment creation fails**
```bash
# Make sure you're in the correct directory
cd tests/e2e_qa
conda env create -f environment.yml
```

**Update environment after dependency changes**
```bash
conda env update -f environment.yml --prune
```

### Configuration Issues

**Missing `.env` file**
```bash
# Create from example
cp env.example .env
# Then edit .env to set OTEL_ENDPOINT and other required variables
```

**`OTEL_ENDPOINT is required` error**
Edit your `.env` file and set the `OTEL_ENDPOINT` variable to your OpenTelemetry collector URL.

### Runtime Issues

**No console output**
Set `OTEL_CONSOLE_EXPORTER=true` in your `.env` file to see telemetry data in the console.

**Data not appearing in backend**
1. Verify `OTEL_CONSOLE_EXPORTER=false` in your `.env` file
2. Check that `OTEL_ENDPOINT` is correctly set
3. Verify network connectivity to the endpoint
4. Ensure examples completed successfully (check for error messages)
5. Wait 1-5 minutes for backend processing
6. Contact your telemetry team for backend access and troubleshooting

## Contributing

1. Review design documents in `_docs/`
2. Follow existing code style
3. Update documentation
4. Submit pull request
