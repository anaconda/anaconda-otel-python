# E2E QA Project - Conda Setup Guide

## Overview

This guide provides detailed instructions for setting up the E2E QA project using **conda**, which is the **recommended installation method** for the `anaconda-opentelemetry` SDK.

---

## Why Conda?

### Advantages
- ✅ **Official Distribution**: SDK is distributed via Anaconda
- ✅ **Dependency Management**: Conda handles all dependencies
- ✅ **Environment Isolation**: Clean, reproducible environments
- ✅ **Version Control**: Easy to manage SDK versions
- ✅ **Cross-Platform**: Works on Windows, macOS, Linux

### Recommended For
- Production use
- Development and testing
- CI/CD pipelines
- Team collaboration
- Reproducible environments

---

## Installation Methods

### Method 1: Quick Start (Recommended)

Create a new conda environment with the SDK in one command:

```bash
# Create environment with SDK and Python 3.10
conda create -n e2e-qa-examples anaconda-opentelemetry python=3.10

# Activate the environment
conda activate e2e-qa-examples

# Navigate to project directory
cd tests/e2e_qa

# Verify installation
python -c "from anaconda.opentelemetry import initialize_telemetry; print('✓ SDK installed successfully')"
```

---

### Method 2: Using Environment File

Create a conda environment from a specification file:

**Step 1**: Create `environment.yml` file:

```yaml
name: e2e-qa-examples
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - anaconda-opentelemetry
  - pip
  # No additional pip dependencies needed for hello-world examples
```

**Step 2**: Create environment from file:

```bash
# Create environment
conda env create -f environment.yml

# Activate environment
conda activate e2e-qa-examples

# Verify installation
python -c "from anaconda.opentelemetry import initialize_telemetry; print('✓ SDK installed successfully')"
```

---

### Method 3: Add to Existing Environment

Add the SDK to an existing conda environment:

```bash
# Activate your existing environment
conda activate your-existing-env

# Install the SDK
conda install anaconda-opentelemetry

# Verify installation
python -c "from anaconda.opentelemetry import initialize_telemetry; print('✓ SDK installed successfully')"
```

---

## Environment Specification

### Minimal Environment

For running examples only:

```yaml
name: e2e-qa-minimal
channels:
  - conda-forge
  - defaults
dependencies:
  - python>=3.9  # SDK requires Python 3.9+
  - anaconda-opentelemetry
```

### Development Environment

For development and testing:

```yaml
name: e2e-qa-dev
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - anaconda-opentelemetry
  - pip
  # No additional pip dependencies needed for hello-world examples
    - black  # Code formatting
    - flake8  # Linting
```

### Full Environment

For complete development setup:

```yaml
name: e2e-qa-full
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - anaconda-opentelemetry
  - pip
  - ipython  # Interactive shell
  - jupyter  # Notebooks (optional)
  # No additional pip dependencies needed for hello-world examples
    - black
    - flake8
    - mypy  # Type checking
```

---

## Verification Steps

### 1. Verify Conda Installation

```bash
# Check conda version
conda --version

# Should output: conda 4.x.x or higher
```

### 2. Verify Environment Creation

```bash
# List all conda environments
conda env list

# Should show e2e-qa-examples in the list
```

### 3. Verify SDK Installation

```bash
# Activate environment
conda activate e2e-qa-examples

# Check installed packages
conda list anaconda-opentelemetry

# Should show package version
```

### 4. Verify SDK Import

```bash
# Test import
python -c "from anaconda.opentelemetry import Configuration, ResourceAttributes, initialize_telemetry; print('✓ All imports successful')"
```

### 5. Verify All SDK Components

```python
# Create test script: verify_sdk.py
from anaconda.opentelemetry import (
    Configuration,
    ResourceAttributes,
    initialize_telemetry,
    increment_counter,
    decrement_counter,
    record_histogram,
    get_trace,
    get_telemetry_logger_handler
)

print("✓ Configuration imported")
print("✓ ResourceAttributes imported")
print("✓ initialize_telemetry imported")
print("✓ increment_counter imported")
print("✓ decrement_counter imported")
print("✓ record_histogram imported")
print("✓ get_trace imported")
print("✓ get_telemetry_logger_handler imported")
print("\n✅ All SDK components verified successfully!")
```

Run verification:
```bash
python verify_sdk.py
```

---

## Running Examples with Conda

### Basic Example Run

```bash
# Activate environment
conda activate e2e-qa-examples

# Navigate to project
cd tests/e2e_qa

# Run all examples
python run_examples.py

# Run specific example
python -m src.metrics_examples
```

### Running Tests

```bash
# Activate environment
conda activate e2e-qa-examples

# Navigate to project
cd tests/e2e_qa

# Run all examples
python run_all_examples.py

# Run specific example
python examples/01_configuration.py

# Run with verbose output
python run_all_examples.py --verbose
```

---

## Environment Management

### List Environments

```bash
# Show all conda environments
conda env list
```

### Activate/Deactivate

```bash
# Activate environment
conda activate e2e-qa-examples

# Deactivate environment
conda deactivate
```

### Update Environment

```bash
# Activate environment
conda activate e2e-qa-examples

# Update SDK to latest version
conda update anaconda-opentelemetry

# Update all packages
conda update --all
```

### Export Environment

```bash
# Export current environment
conda env export > environment.yml

# Export without builds (more portable)
conda env export --no-builds > environment.yml

# Export only explicit packages
conda env export --from-history > environment.yml
```

### Clone Environment

```bash
# Clone existing environment
conda create --name e2e-qa-examples-clone --clone e2e-qa-examples
```

### Remove Environment

```bash
# Deactivate if active
conda deactivate

# Remove environment
conda env remove -n e2e-qa-examples
```

---

## Troubleshooting

### Issue: SDK Not Found

```bash
# Problem: ImportError: No module named 'anaconda.opentelemetry'

# Solution 1: Verify environment is activated
conda activate e2e-qa-examples

# Solution 2: Reinstall SDK
conda install --force-reinstall anaconda-opentelemetry

# Solution 3: Check conda channels
conda config --show channels
```

### Issue: Wrong Python Version

```bash
# Problem: Python version incompatible

# Solution: Create new environment with correct Python
conda create -n e2e-qa-examples anaconda-opentelemetry python=3.10
```

### Issue: Dependency Conflicts

```bash
# Problem: Conda cannot resolve dependencies

# Solution 1: Update conda
conda update conda

# Solution 2: Use conda-forge channel
conda install -c conda-forge anaconda-opentelemetry

# Solution 3: Create fresh environment
conda create -n e2e-qa-examples-new anaconda-opentelemetry
```

### Issue: Environment Not Activating

```bash
# Problem: conda activate not working

# Solution 1: Initialize conda for your shell
conda init bash  # or zsh, fish, etc.

# Solution 2: Use source activate (older conda)
source activate e2e-qa-examples

# Solution 3: Restart shell
exec $SHELL
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E QA Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Miniconda
        uses: conda-incubator/setup-miniconda@v2
        with:
          auto-update-conda: true
          python-version: 3.10
          
      - name: Install SDK
        run: |
          conda install anaconda-opentelemetry
          
      - name: Run examples
        run: |
          cd tests/e2e_qa
          python run_all_examples.py
```

### GitLab CI Example

```yaml
test:
  image: continuumio/miniconda3
  script:
    - conda install anaconda-opentelemetry
    - cd tests/e2e_qa
    - python run_all_examples.py
```

---

## Best Practices

### 1. Use Environment Files
- ✅ Create `environment.yml` for reproducibility
- ✅ Commit to version control
- ✅ Update when dependencies change

### 2. Pin Versions
```yaml
dependencies:
  - python=3.10.8
  - anaconda-opentelemetry=1.2.3
```

### 3. Separate Environments
- Development: `e2e-qa-dev`
- Testing: `e2e-qa-examples`
- Production: `e2e-qa-prod`

### 4. Regular Updates
```bash
# Update SDK regularly
conda update anaconda-opentelemetry
```

### 5. Clean Unused Environments
```bash
# Remove unused environments
conda env remove -n old-env-name

# Clean package cache
conda clean --all
```

---

## Quick Reference

### Essential Commands

```bash
# Create environment
conda create -n e2e-qa-examples anaconda-opentelemetry python=3.10

# Activate environment
conda activate e2e-qa-examples

# Verify installation
python -c "from anaconda.opentelemetry import initialize_telemetry; print('OK')"

# Run examples
python run_examples.py

# Run examples
python run_all_examples.py

# Deactivate
conda deactivate
```

---

## Additional Resources

### Documentation
- [Conda User Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/)
- [Anaconda OpenTelemetry Docs](../../docs/source/getting_started.md)
- [E2E QA README](../README.md)

### Support
- Conda issues: https://github.com/conda/conda/issues
- SDK issues: Project repository issues

---

**Last Updated**: 2026-01-16
**Conda Version**: 4.x or higher recommended
**Python Version**: See [REQUIREMENTS.md](REQUIREMENTS.md) for version details
