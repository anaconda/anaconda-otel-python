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
├── _docs/                          # Design specifications
│   ├── 00_summary.md              # Project summary
│   ├── 01_requirements.md          # Requirements (authoritative)
│   ├── 02_architecture_design.md   # Technical architecture
│   ├── 03_implementation_plan.md   # Development phases
│   ├── 04_test_scenarios.md        # Example scenarios
│   ├── 05_visual_guide.md          # Visual diagrams
│   ├── 06_conda_setup.md           # Conda setup guide
│   ├── 07_environment_configuration.md  # Environment & endpoint config
│   └── INDEX.md                    # Documentation index
│
├── examples/                       # Example implementations
│   ├── 01_config_examples.py       # Configuration examples
│   ├── 02_attributes_examples.py   # ResourceAttributes examples
│   ├── 01_all_signals.py           # Init: All signals
│   ├── 02_metrics_only.py          # Init: Metrics only
│   ├── 03_default.py               # Init: Default config
│   ├── 04_selective.py             # Init: Selective signals
│   ├── 05_complete.py              # Init: Complete setup
│   └── 06_env_based.py             # Init: Environment-based
│
├── .env                            # Environment configuration (create from env.example)
├── env.example                     # Example environment configuration
├── environment.yml                 # Conda environment specification
├── README.md                       # This file
└── run_all_examples.py             # Main entry point (to be created)
```

## Quick Start

### Prerequisites

- **Conda** package manager installed
- **Python 3.9+** (3.10 recommended)
- **Git** (to clone the repository)

### Setup

1. **Create and activate conda environment**
   ```bash
   cd tests/e2e_qa
   conda env create -f environment.yml
   conda activate e2e-qa-examples
   ```

2. **Install SDK in development mode**
   ```bash
   cd ../..  # Go to repo root
   pip install -e .
   ```

3. **Configure environment**
   ```bash
   cd tests/e2e_qa
   cp env.example .env
   ```
   
   **For Backend Validation**:
   ```bash
   # Edit .env - CRITICAL: Set console exporter to false
   OTEL_CONSOLE_EXPORTER=false  # Data goes to backend
   OTEL_ENVIRONMENT=staging-internal
   ```
   
   **For Local Debugging**:
   ```bash
   # Edit .env - Console output only (no backend)
   OTEL_CONSOLE_EXPORTER=true  # Data printed to console only
   ```

   ⚠️ **Critical**: Console exporter and backend are mutually exclusive! Set to `false` for backend validation.
   
   ⚠️ **Important**: Only send test data to staging environments. See [07_environment_configuration.md](_docs/07_environment_configuration.md) for details.

4. **Verify installation**
   ```bash
   python -c "from anaconda.opentelemetry import Configuration, ResourceAttributes, initialize_telemetry; print('✓ SDK imported successfully')"
   ```

### Running Examples

#### 🚀 Recommended Usage

**For backend validation** (sends data to backend):
```bash
# Run all 6 initialization examples (each in separate process)
python run_initialization_examples.py
```

**For full SDK demonstration** (config + attributes + initialization):
```bash
# Run all example categories
python run_all_examples.py
```

**For single example**:
```bash
# Run one initialization example
python examples/01_all_signals.py

# Or run config/attributes examples (no backend data)
python examples/01_config_examples.py
python examples/02_attributes_examples.py
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

### 3. Initialization Examples - Choosing the Right Approach

**Note**: Each example runs in a separate process to ensure proper initialization.

Run all 6 examples: `python run_initialization_examples.py`

#### Example Types: Atomic vs. Complex

These examples follow a **progressive learning approach** with two types:

**ATOMIC EXAMPLES** (Examples 1-4): Learn one concept at a time
- **Purpose**: Demonstrate a single initialization pattern clearly
- **Best for**: Quick reference, copy-paste templates, learning basics
- **When to use**: You know exactly what you need and want a simple starting point

**COMPLEX EXAMPLES** (Examples 5-6): See everything working together
- **Purpose**: Show production-ready configurations with multiple options
- **Best for**: Understanding real-world usage, comprehensive setups
- **When to use**: You need advanced configuration or want to see all features

#### Individual Examples

##### Atomic Examples - Single Concept Focus

- **`examples/01_all_signals.py`** - Initialize with all signals (metrics, logs, traces)
  - **Use when**: You need comprehensive observability across all signal types
  - **Best for**: Production microservices, complex applications needing full visibility
  - **Copy this if**: You want complete telemetry coverage

- **`examples/02_metrics_only.py`** - Initialize with metrics only
  - **Use when**: You only need counters, gauges, and histograms
  - **Best for**: Batch jobs, background workers, simple monitoring
  - **Copy this if**: You want minimal overhead and only need metrics

- **`examples/03_default.py`** - Default initialization (implicit metrics)
  - **Use when**: You want the simplest possible setup with SDK defaults
  - **Best for**: Quick prototyping, learning basics, simple scripts
  - **Copy this if**: You prefer concise code and default behavior is sufficient

- **`examples/04_selective.py`** - Selective signals (metrics + tracing)
  - **Use when**: You need specific signal combinations, not all or just one
  - **Best for**: Services needing request tracing and metrics but not logging
  - **Copy this if**: You want to balance observability with resource constraints

##### Complex Examples - Production-Ready Patterns

- **`examples/05_complete.py`** - Complete configuration with all options
  - **Use when**: You need fine-grained control over all configuration aspects
  - **Best for**: Production services with specific export intervals, logging levels, custom attributes
  - **Copy this if**: You need a comprehensive reference showing all SDK capabilities

- **`examples/06_env_based.py`** - Environment-based initialization
  - **Use when**: Your app runs in multiple environments (dev/staging/prod)
  - **Best for**: Multi-environment deployments using 12-factor configuration
  - **Copy this if**: You need environment-aware telemetry with dynamic configuration

#### Quick Selection Guide

| Your Need | Start With | Why |
|-----------|------------|-----|
| "I need everything" | `01_all_signals.py` | All signals enabled, simple setup |
| "Just metrics" | `02_metrics_only.py` | Minimal overhead, focused |
| "Simplest possible" | `03_default.py` | Fewest lines of code |
| "Metrics + tracing only" | `04_selective.py` | Specific signal combination |
| "Production config" | `05_complete.py` | All configuration options |
| "Multi-environment" | `06_env_based.py` | Environment-aware setup |

**Critical**: Each example force flushes to ensure data reaches backend.

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

When you run the examples, you'll see clear output showing:
- SDK method calls being executed
- Success indicators
- Flush confirmation messages

**For backend validation**: See **[08_backend_validation.md](_docs/08_backend_validation.md)** for complete step-by-step validation guide including:
- Expected metrics in backend
- SQL queries for verification
- Resource attributes validation
- Troubleshooting steps

## Documentation

See `_docs/` directory for:
- Architecture and design
- Implementation plan
- Detailed scenarios
- Environment configuration
- Documentation index

Key documents:
- **[07_environment_configuration.md](_docs/07_environment_configuration.md)** - Environment and endpoint configuration guide
- **[08_backend_validation.md](_docs/08_backend_validation.md)** - Backend validation and verification guide
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

**`ModuleNotFoundError: No module named 'anaconda'`**
```bash
# Install SDK in development mode from repo root
cd /path/to/anaconda-otel-python
pip install -e .
```

**`ModuleNotFoundError: No module named 'dotenv'`**
```bash
pip install python-dotenv
```

**Conda environment creation fails**
```bash
# Make sure you're in the correct directory
cd tests/e2e_qa
conda env create -f environment.yml
```

**"No access to endpoint" warning**
This is expected if you're not connected to VPN/WARP. Examples will still run with console output. To suppress:
```bash
# Add to .env file
OTEL_SKIP_INTERNET_CHECK=true
```

**No console output**
Ensure `config.set_console_exporter(use_console=True)` in your code.

**Data not appearing in backend**

See **[08_backend_validation.md](_docs/08_backend_validation.md)** for complete troubleshooting guide including:
- Console exporter configuration (must be disabled for backend)
- Flush requirements
- WARP/VPN connection
- Backend query examples

**Update environment after dependency changes**
```bash
conda env update -f environment.yml --prune
```

## Contributing

1. Review design documents in `_docs/`
2. Follow existing code style
3. Update documentation
4. Submit pull request
