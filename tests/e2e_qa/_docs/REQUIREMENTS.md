# E2E QA Project - Requirements

**Authoritative source for all project requirements**

---

## Python Version Requirements

### Minimum Version
**Python 3.9+** (required by SDK)

Source: `anaconda-otel-python/pyproject.toml` line 28:
```toml
requires-python = ">=3.9"
```

### Recommended Version
**Python 3.10**

Rationale:
- Above minimum requirement (3.9+)
- Widely supported in production
- Stable and mature
- Good ecosystem compatibility
- Used in all SDK CI/CD tests

### Supported Versions
All versions tested in SDK CI/CD (`.github/workflows/ci.yaml`):

| Python Version | Status | Notes |
|---------------|--------|-------|
| 3.8 | ❌ Not Supported | Below minimum |
| 3.9 | ✅ Minimum | Required |
| 3.10 | ✅ **Recommended** | Best choice |
| 3.11 | ✅ Supported | Fully compatible |
| 3.12 | ✅ Supported | Latest stable |
| 3.13 | ✅ Supported | Newest version |

---

## Package Manager

### Required
**conda** (Anaconda package manager)

Rationale:
- **Only installation method documented by SDK**
- Official Anaconda distribution
- Better dependency management
- Environment isolation
- Cross-platform support

Source: SDK `docs/source/getting_started.md` only documents conda installation.

### Note on pip
pip is **not documented** as an installation method in the main SDK documentation. While the package may be pip-installable (as it has a `pyproject.toml`), conda is the official and supported method.

---

## Dependencies

### Core Dependency
- `anaconda-opentelemetry` (the SDK being tested)

### Test Dependencies
- `pytest>=7.0.0` - Test framework
- `pytest-cov>=4.0.0` - Coverage reporting

### Optional Development Dependencies
- `black` - Code formatting
- `flake8` - Linting
- `mypy` - Type checking

---

## Installation Commands

### Quick Start (Recommended)
```bash
conda create -n e2e-qa-test anaconda-opentelemetry python=3.10
conda activate e2e-qa-test
pip install pytest pytest-cov
```

### Minimum Version
```bash
conda create -n e2e-qa-test anaconda-opentelemetry python=3.9
```

### Using Environment File
```bash
conda env create -f environment.yml.template
```

---

**Note**: All other documentation files reference this file for requirements.
**Last Updated**: 2026-01-16
