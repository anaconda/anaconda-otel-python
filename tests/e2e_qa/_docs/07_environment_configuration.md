# E2E QA Project - Environment Configuration

## Overview

This document describes the supported environments for sending telemetry data. **Only send test data to staging environments.** Production endpoints are documented for reference but should only be used with real production data and proper authentication.

## Environment File

Configuration is managed through a `.env` file located in `tests/e2e_qa/.env`. This file contains environment variables that control which endpoint to use.

### Setup

1. Copy the `env.example` file to `.env`:
   ```bash
   cd tests/e2e_qa
   cp env.example .env
   ```

2. Edit `.env` to set your desired environment:
   ```bash
   # Choose your environment based on your access method:
   # - staging-internal: Behind WARP VPN (default for local development)
   # - staging-internal-gha: From GitHub Actions or internal services (no WARP)
   # - staging-public: OAuth testing (behind WARP)
   # - production-external: Real production data with API key
   # - production-internal: Real production data from internal services
   
   OTEL_ENVIRONMENT=staging-internal
   
   # Endpoint will be automatically selected based on OTEL_ENVIRONMENT
   # Or you can override with a custom endpoint:
   # OTEL_ENDPOINT=https://custom-endpoint.example.com/v1/metrics
   ```

## Supported Environments

### Staging Environments (For Testing Only)

#### Staging - Internal

**Use Case**: Development and testing from internal services, GitHub runners, or behind WARP

**Endpoints**:

1. **Behind WARP** (requires WARP connection):
   ```
   https://metrics.stage.anacondaconnect.com/v1/metrics
   ```

2. **Internal Services** (unauthenticated, from GitHub runners or internal services):
   ```
   https://metrics.stage.internal.anacondaconnect.com/v1/metrics
   ```

3. **Kubernetes Internal** (dev cluster, avoids external traffic):
   ```
   http://metrics-collector.opentelemetry.svc.cluster.local
   ```

**Authentication**: None required

**Environment Variable**:
```bash
OTEL_ENVIRONMENT=staging-internal
```

#### Staging - Public (OAuth Test Endpoint)

**Use Case**: Testing OAuth authentication flow

**Endpoint**:
```
https://metrics.stage-oauth.anacondaconnect.com/v1/metrics
```

**Authentication**: OIDC via auth service

**Current Status**: Behind WARP for testing phase

**Environment Variable**:
```bash
OTEL_ENVIRONMENT=staging-public
```

**Important**: This is currently a test endpoint only.

---

### Production Environments (Real Data Only)

⚠️ **WARNING**: Production endpoints should only be used with real production data. Do not send test data to production.

#### Production - External

**Use Case**: External services and applications requiring authenticated access

**Endpoints**:

1. **Standard Production** (requires API key):
   ```
   https://metrics.anaconda.com/v1/metrics
   ```

2. **Behind WARP** (requires WARP connection):
   ```
   https://metrics.w.anaconda.com/v1/metrics
   ```

**Authentication**: API key required (use SendSafely for secure transmission)

**Environment Variable**:
```bash
OTEL_ENVIRONMENT=production-external
```

#### Production - Internal

**Use Case**: Internal services, self-hosted GitHub runners, internal cluster workloads

**Endpoints**:

1. **Internal Services** (no WARP required):
   ```
   https://metrics.internal.anaconda.com/v1/metrics
   ```

2. **Kubernetes Internal** (prod cluster, avoids external traffic):
   ```
   http://metrics-collector.opentelemetry.svc.cluster.local
   ```

**Authentication**: None required for internal services

**Environment Variable**:
```bash
OTEL_ENVIRONMENT=production-internal
```

---

## Configuration in Code

### Loading Environment Variables

```python
import os
from dotenv import load_dotenv
from anaconda.opentelemetry import Configuration, ResourceAttributes, initialize_telemetry

# Load environment variables from .env file
load_dotenv()

# Get environment and endpoint
environment = os.getenv('OTEL_ENVIRONMENT', 'staging-internal')
custom_endpoint = os.getenv('OTEL_ENDPOINT')

# Environment to endpoint mapping
ENDPOINTS = {
    'staging-internal': 'https://metrics.stage.internal.anacondaconnect.com/v1/metrics',
    'staging-public': 'https://metrics.stage-oauth.anacondaconnect.com/v1/metrics',
    'production-external': 'https://metrics.anaconda.com/v1/metrics',
    'production-internal': 'https://metrics.internal.anaconda.com/v1/metrics',
}

# Use custom endpoint if provided, otherwise use environment mapping
endpoint = custom_endpoint or ENDPOINTS.get(environment)

# Create configuration
config = Configuration(default_endpoint=endpoint)
```

### Complete Example

```python
import os
from dotenv import load_dotenv
from anaconda.opentelemetry import (
    Configuration,
    ResourceAttributes,
    initialize_telemetry,
    increment_counter
)

def setup_telemetry():
    """Setup telemetry with environment-based configuration"""
    # Load .env file
    load_dotenv()
    
    # Get configuration from environment
    environment = os.getenv('OTEL_ENVIRONMENT', 'staging-internal')
    
    # Endpoint mapping
    endpoints = {
        'staging-internal': 'https://metrics.stage.internal.anacondaconnect.com/v1/metrics',
        'staging-public': 'https://metrics.stage-oauth.anacondaconnect.com/v1/metrics',
        'production-external': 'https://metrics.anaconda.com/v1/metrics',
        'production-internal': 'https://metrics.internal.anaconda.com/v1/metrics',
    }
    
    endpoint = os.getenv('OTEL_ENDPOINT') or endpoints.get(environment)
    
    if not endpoint:
        raise ValueError(f"Unknown environment: {environment}")
    
    print(f"Using environment: {environment}")
    print(f"Endpoint: {endpoint}")
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    
    # Optional: Enable console output for debugging
    if os.getenv('OTEL_CONSOLE_EXPORTER', 'false').lower() == 'true':
        config.set_console_exporter(use_console=True)
    
    # Create resource attributes
    attrs = ResourceAttributes(
        service_name="e2e-qa-examples",
        service_version="1.0.0"
    )
    
    # Add environment information
    attrs.set_attributes({
        'environment': environment,
        'test.type': 'e2e-qa'
    })
    
    # Initialize telemetry
    initialize_telemetry(config, attrs, signals=['metrics', 'logs', 'traces'])
    
    return config, attrs

if __name__ == "__main__":
    # Setup telemetry
    config, attrs = setup_telemetry()
    
    # Send a test metric
    increment_counter(
        "e2e_qa.test_counter",
        by=1,
        attributes={"test": "environment_setup"}
    )
    
    print("✓ Telemetry setup complete and test metric sent")
```

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OTEL_ENVIRONMENT` | No | `staging-internal` | Environment name (staging-internal, staging-public, production-external, production-internal) |
| `OTEL_ENDPOINT` | No | (auto-selected) | Custom endpoint URL (overrides environment-based selection) |
| `OTEL_CONSOLE_EXPORTER` | No | `false` | Enable console output for debugging (`true`/`false`) |
| `OTEL_API_KEY` | Conditional | - | API key for production-external (required for that environment) |

## Best Practices

### 1. Default to Staging for Testing

Always use staging environments for development and testing:

```bash
# .env
OTEL_ENVIRONMENT=staging-internal
```

### 2. Never Commit .env Files

Add `.env` to `.gitignore`:

```gitignore
# Environment configuration
.env
```

### 3. Use env.example for Documentation

Provide an `env.example` file with safe defaults:

```bash
# env.example
OTEL_ENVIRONMENT=staging-internal
OTEL_CONSOLE_EXPORTER=true
# OTEL_ENDPOINT=  # Optional: custom endpoint override
```

### 4. Validate Environment Configuration

Add validation to catch configuration errors early:

```python
def validate_environment():
    """Validate environment configuration"""
    environment = os.getenv('OTEL_ENVIRONMENT', 'staging-internal')
    
    # Warn if using production
    if environment.startswith('production'):
        print("⚠️  WARNING: Using production environment!")
        print("   Only send real production data to production endpoints.")
        response = input("   Continue? (yes/no): ")
        if response.lower() != 'yes':
            raise ValueError("Production environment usage cancelled")
    
    return environment
```

### 5. Environment-Specific Attributes

Tag telemetry data with environment information:

```python
attrs = ResourceAttributes("e2e-qa-examples", "1.0.0")
attrs.set_attributes({
    'environment': os.getenv('OTEL_ENVIRONMENT', 'staging-internal'),
    'deployment.environment': 'test',
    'test.type': 'e2e-qa'
})
```

## Network Requirements

### Staging - Internal
- **WARP endpoint**: Requires WARP VPN connection
- **Internal endpoint**: Accessible from GitHub runners and internal services
- **Kubernetes endpoint**: Only accessible from within dev cluster

### Staging - Public
- **Currently**: Requires WARP (testing phase)
- **Future**: Will be publicly accessible with OAuth

### Production - External
- **Standard**: Requires API key, accessible from anywhere
- **WARP**: Requires WARP VPN connection

### Production - Internal
- **Internal endpoint**: Accessible from self-hosted runners and internal services
- **Kubernetes endpoint**: Only accessible from within prod cluster

## Troubleshooting

### Connection Issues

**Problem**: Cannot connect to endpoint

**Solutions**:
1. Check if WARP is required and connected
2. Verify endpoint URL is correct
3. Check network connectivity
4. Verify authentication (for production-external)

### Authentication Errors

**Problem**: 401 Unauthorized or 403 Forbidden

**Solutions**:
1. Verify API key is set (for production-external)
2. Check OIDC authentication (for staging-public)
3. Ensure using correct endpoint for your context

### Wrong Environment

**Problem**: Accidentally using production

**Solutions**:
1. Check `.env` file
2. Add validation code (see Best Practices)
3. Use environment-specific naming in service attributes

## Related Documentation

- **[01_requirements.md](01_requirements.md)** - Python and dependency requirements
- **[02_architecture_design.md](02_architecture_design.md)** - Architecture overview
- **[03_implementation_plan.md](03_implementation_plan.md)** - Implementation details
- **[README.md](../README.md)** - Quick start guide

---

**Last Updated**: 2026-01-16
