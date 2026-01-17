# OpenTelemetry Endpoints Quick Reference

⚠️ **IMPORTANT**: Only send test data to staging environments!

## Quick Setup

```bash
# 1. Copy environment template
cp env.example .env

# 2. Edit .env and set OTEL_ENVIRONMENT
# Default: staging-internal (recommended for testing)
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OTEL_ENVIRONMENT` | `staging-internal` | Environment name |
| `OTEL_ENDPOINT` | (auto) | Custom endpoint (optional) |
| `OTEL_CONSOLE_EXPORTER` | `true` | Enable console output |
| `OTEL_API_KEY` | - | API key (production-external only) |

## Endpoints Quick Reference

### 🧪 Staging - Internal (Default for Testing)

```bash
OTEL_ENVIRONMENT=staging-internal
```

| Access Method | Endpoint | Auth Required |
|--------------|----------|---------------|
| Behind WARP | `https://metrics.stage.anacondaconnect.com/v1/metrics` | No |
| Internal/GHA | `https://metrics.stage.internal.anacondaconnect.com/v1/metrics` | No |
| K8s (dev) | `http://metrics-collector.opentelemetry.svc.cluster.local` | No |

**Use for**: Development, testing, CI/CD

---

### 🧪 Staging - Public (OAuth Testing)

```bash
OTEL_ENVIRONMENT=staging-public
```

| Access Method | Endpoint | Auth Required |
|--------------|----------|---------------|
| OAuth Test | `https://metrics.stage-oauth.anacondaconnect.com/v1/metrics` | OIDC |

**Status**: Currently behind WARP (testing phase)

**Use for**: OAuth authentication testing

---

### 🚀 Production - External

```bash
OTEL_ENVIRONMENT=production-external
OTEL_API_KEY=your-api-key-here
```

| Access Method | Endpoint | Auth Required |
|--------------|----------|---------------|
| Standard | `https://metrics.anaconda.com/v1/metrics` | API Key |
| Behind WARP | `https://metrics.w.anaconda.com/v1/metrics` | API Key |

**Use for**: Real production data from external services

⚠️ **Requires API key** - Use SendSafely for secure transmission

---

### 🚀 Production - Internal

```bash
OTEL_ENVIRONMENT=production-internal
```

| Access Method | Endpoint | Auth Required |
|--------------|----------|---------------|
| Internal | `https://metrics.internal.anaconda.com/v1/metrics` | No |
| K8s (prod) | `http://metrics-collector.opentelemetry.svc.cluster.local` | No |

**Use for**: Real production data from internal services/GHA runners

---

## Code Example

```python
import os
from dotenv import load_dotenv
from anaconda.opentelemetry import Configuration, ResourceAttributes, initialize_telemetry

# Load environment
load_dotenv()

# Environment mapping
ENDPOINTS = {
    'staging-internal': 'https://metrics.stage.internal.anacondaconnect.com/v1/metrics',
    'staging-public': 'https://metrics.stage-oauth.anacondaconnect.com/v1/metrics',
    'production-external': 'https://metrics.anaconda.com/v1/metrics',
    'production-internal': 'https://metrics.internal.anaconda.com/v1/metrics',
}

# Get endpoint
env = os.getenv('OTEL_ENVIRONMENT', 'staging-internal')
endpoint = os.getenv('OTEL_ENDPOINT') or ENDPOINTS[env]

# Configure
config = Configuration(default_endpoint=endpoint)
attrs = ResourceAttributes("my-service", "1.0.0")
initialize_telemetry(config, attrs)
```

## Network Requirements

| Environment | WARP Required | Internal Network | K8s Cluster |
|------------|---------------|------------------|-------------|
| staging-internal (WARP) | ✅ | ❌ | ❌ |
| staging-internal (Internal) | ❌ | ✅ | ❌ |
| staging-internal (K8s) | ❌ | ❌ | ✅ (dev) |
| staging-public | ✅ (currently) | ❌ | ❌ |
| production-external | ❌ | ❌ | ❌ |
| production-external (WARP) | ✅ | ❌ | ❌ |
| production-internal | ❌ | ✅ | ❌ |
| production-internal (K8s) | ❌ | ❌ | ✅ (prod) |

## Troubleshooting

### Cannot connect to endpoint

1. Check WARP connection (if required)
2. Verify endpoint URL in `.env`
3. Check network connectivity
4. Verify API key (production-external)

### Using wrong environment

1. Check `.env` file: `cat .env`
2. Verify `OTEL_ENVIRONMENT` value
3. Add validation in code (see full docs)

## Full Documentation

See [07_environment_configuration.md](_docs/07_environment_configuration.md) for:
- Detailed setup instructions
- Complete code examples
- Best practices
- Security considerations
- Advanced configuration

---

**Last Updated**: 2026-01-16
