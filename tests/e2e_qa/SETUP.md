# E2E QA Examples - Setup Guide

Quick guide to get the E2E QA examples running on your machine.

## Prerequisites

- **Conda** package manager installed
- **Python 3.9+** (3.10 recommended)
- **Git** (to clone the repository)

## Setup Steps

### 1. Create Conda Environment

```bash
cd tests/e2e_qa
conda env create -f environment.yml
```

This creates a new conda environment named `e2e-qa-examples` with all required dependencies.

### 2. Activate the Environment

```bash
conda activate e2e-qa-examples
```

### 3. Install the SDK in Development Mode

From the repository root:

```bash
cd ../..  # Go to repo root
pip install -e .
```

This installs the `anaconda-opentelemetry` package in editable mode, so any changes to the SDK code are immediately reflected.

### 4. Configure Environment

```bash
cd tests/e2e_qa
cp env.example .env
```

Edit `.env` if you want to change the default environment (staging-internal):

```bash
# Optional: Edit .env to change settings
# OTEL_ENVIRONMENT=staging-internal  # Default
# OTEL_CONSOLE_EXPORTER=true         # Show telemetry in console
```

### 5. Run Examples

```bash
# Run all examples
python run_all_examples.py

# Or run individual examples
cd examples
python 01_config_examples.py
python 02_attributes_examples.py
python 03_initialization_examples.py
```

## Verification

Test that everything is working:

```bash
python -c "
from anaconda.opentelemetry import Configuration, ResourceAttributes, initialize_telemetry
print('✓ SDK imported successfully')
"
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'anaconda'`

**Solution**: Make sure you installed the SDK in development mode:
```bash
cd /path/to/anaconda-otel-python
pip install -e .
```

### Issue: `ModuleNotFoundError: No module named 'dotenv'`

**Solution**: Install python-dotenv:
```bash
pip install python-dotenv
```

### Issue: Conda environment creation fails

**Solution**: Make sure you're using the correct file name:
```bash
conda env create -f environment.yml  # Not environment.yml.template
```

### Issue: "No access to endpoint" warning

**Solution**: This is expected if you're not connected to VPN/WARP. The examples will still run and show console output. To suppress this warning, set in `.env`:
```bash
OTEL_SKIP_INTERNET_CHECK=true
```

## Environment Details

The conda environment includes:
- Python 3.10
- python-dotenv (for .env file support)
- OpenTelemetry SDK and exporters
- All required dependencies

## Next Steps

After setup, explore the examples:
1. Start with `01_config_examples.py` to understand configuration
2. Move to `02_attributes_examples.py` for resource attributes
3. Try `03_initialization_examples.py` for initialization patterns

See [README.md](README.md) for detailed documentation.

## Updating the Environment

If dependencies change, update your environment:

```bash
conda env update -f environment.yml --prune
```

## Removing the Environment

When you're done:

```bash
conda deactivate
conda env remove -n e2e-qa-examples
```

---

**Questions?** Check the [README.md](README.md) or [documentation](_docs/INDEX.md).
