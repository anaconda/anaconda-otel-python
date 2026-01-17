# E2E QA Project - Conda Setup Guide

## Overview

Setup guide for the E2E QA project using conda (recommended for `anaconda-opentelemetry` SDK).

## Why Conda?

- Official SDK distribution method
- Handles dependencies automatically
- Environment isolation
- Cross-platform support

## Installation

### Quick Start
```bash
conda create -n e2e-qa-examples anaconda-opentelemetry python=3.10
conda activate e2e-qa-examples
cd tests/e2e_qa
```

### Using Environment File
```bash
conda env create -f environment.yml
conda activate e2e-qa-examples
```

### Add to Existing Environment
```bash
conda activate your-env
conda install anaconda-opentelemetry
```

## Environment Specification

Minimal setup:
```yaml
name: e2e-qa-examples
dependencies:
  - python=3.10
  - anaconda-opentelemetry
```

## Verification

```bash
conda activate e2e-qa-examples
conda list anaconda-opentelemetry
python -c "from anaconda.opentelemetry import initialize_telemetry; print('OK')"
```

## Environment Management

```bash
# List environments
conda env list

# Activate/deactivate
conda activate e2e-qa-examples
conda deactivate

# Update SDK
conda update anaconda-opentelemetry

# Remove environment
conda env remove -n e2e-qa-examples
```

## Troubleshooting

**SDK not found**: 
```bash
conda activate e2e-qa-examples
conda install --force-reinstall anaconda-opentelemetry
```

**Wrong Python version**:
```bash
conda create -n e2e-qa-examples anaconda-opentelemetry python=3.10
```

**Environment not activating**:
```bash
conda init bash  # or zsh, fish, etc.
```

## Quick Reference

```bash
# Create and activate
conda create -n e2e-qa-examples anaconda-opentelemetry python=3.10
conda activate e2e-qa-examples

# Verify
python -c "from anaconda.opentelemetry import initialize_telemetry; print('OK')"

# Run
python run_all_examples.py
```
