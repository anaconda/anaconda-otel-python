# E2E QA Backend Validation Guide

**Purpose**: This document describes what to verify in the staging backend after running the E2E QA examples to ensure telemetry data is being correctly received and processed.

**Last Updated**: 2026-01-16

---

## Overview

After running the examples, telemetry data should be visible in the staging backend systems. This guide helps you verify that:
1. Data is arriving at the collector
2. Data is correctly formatted
3. All attributes are present
4. Metrics are aggregated properly

## Prerequisites

- Examples have been run successfully (see `run_all_examples.py`)
- Access to staging backend/observability tools
- WARP VPN connection active
- Note the session ID from the console output for filtering

## Quick Verification Checklist

Use this checklist for a quick validation:

- [ ] Metrics are visible in backend within 60 seconds
- [ ] All 6 test metrics from initialization examples are present
- [ ] Resource attributes match expected values
- [ ] Session ID is consistent across metrics
- [ ] Timestamps are recent and correct
- [ ] No error logs in collector

---

## Phase 1: Configuration Examples Validation

**File**: `examples/01_config_examples.py`

### What to Verify

Configuration examples don't send metrics, but they test:

| Example | What It Tests | Backend Validation |
|---------|---------------|-------------------|
| Example 1 | Basic configuration | N/A - No metrics sent |
| Example 2 | Console exporter | N/A - Local output only |
| Example 3 | Signal-specific endpoints | N/A - No metrics sent |
| Example 4 | Export intervals | N/A - No metrics sent |
| Example 5 | Logging level | N/A - No metrics sent |
| Example 6 | Session entropy | N/A - No metrics sent |
| Example 7 | Skip internet check | N/A - No metrics sent |
| Example 8 | Cumulative metrics | N/A - No metrics sent |
| Example 9 | Complete configuration | N/A - No metrics sent |

**Note**: Configuration examples demonstrate SDK configuration but don't initialize telemetry or send data.

---

## Phase 2: Attributes Examples Validation

**File**: `examples/02_attributes_examples.py`

### What to Verify

Attributes examples don't send metrics, but they test:

| Example | What It Tests | Backend Validation |
|---------|---------------|-------------------|
| Example 1 | Basic ResourceAttributes | N/A - No metrics sent |
| Example 2 | Optional fields | N/A - No metrics sent |
| Example 3 | Auto-populated fields | N/A - No metrics sent |
| Example 4 | set_attributes() method | N/A - No metrics sent |
| Example 5 | Update existing attributes | N/A - No metrics sent |
| Example 6 | Environment-specific attributes | N/A - No metrics sent |
| Example 7 | User identification | N/A - No metrics sent |
| Example 8 | Complete attributes | N/A - No metrics sent |
| Example 9 | Attribute validation | N/A - No metrics sent |

**Note**: Attributes examples demonstrate ResourceAttributes configuration but don't initialize telemetry or send data.

---

## Phase 3: Initialization Examples Validation

**File**: `examples/03_initialization_examples.py`

### Overview

These examples initialize telemetry and send test metrics. **This is where backend validation is critical.**

### Expected Metrics

After running initialization examples, you should see **6 test metrics** in the backend:

1. `example_01_initialization_test`
2. `example_02_metrics_test`
3. `example_03_default_test`
4. `example_04_selective_test`
5. `example_05_complete_test`
6. `example_06_env_based_test`

### Detailed Validation

#### Example 1: Initialize All Signals

**Metric Name**: `example_01_initialization_test`

**Expected in Backend**:
```json
{
  "metric_name": "example_01_initialization_test",
  "value": 1,
  "type": "counter",
  "resource_attributes": {
    "service.name": "example-01-all-signals",
    "service.version": "1.0.0",
    "os.type": "Darwin",  // or "Linux", "Windows"
    "python.version": "3.x.x",
    "client.sdk.version": "0.0.0.devbuild",
    "schema.version": "0.3.0",
    "environment": "",
    "session.id": "<unique-hash>"
  },
  "attributes": {}
}
```

**Verify**:
- ✓ Metric appears within 60 seconds
- ✓ Value is exactly 1
- ✓ Service name is "example-01-all-signals"
- ✓ All resource attributes are present
- ✓ Session ID is a valid hash

---

#### Example 2: Initialize Metrics Only

**Metric Name**: `example_02_metrics_test`

**Expected in Backend**:
```json
{
  "metric_name": "example_02_metrics_test",
  "value": 1,
  "type": "counter",
  "resource_attributes": {
    "service.name": "example-02-metrics-only",
    "service.version": "1.0.0",
    "session.id": "<same-as-example-1>"
  },
  "attributes": {}
}
```

**Verify**:
- ✓ Metric appears within 60 seconds
- ✓ Service name is "example-02-metrics-only"
- ✓ Session ID matches Example 1 (same session)

---

#### Example 3: Default Initialization

**Metric Name**: `example_03_default_test`

**Expected in Backend**:
```json
{
  "metric_name": "example_03_default_test",
  "value": 1,
  "type": "counter",
  "resource_attributes": {
    "service.name": "example-03-default",
    "service.version": "1.0.0"
  },
  "attributes": {}
}
```

**Verify**:
- ✓ Metric appears within 60 seconds
- ✓ Service name is "example-03-default"
- ✓ Default behavior (metrics only) is working

---

#### Example 4: Selective Signals

**Metric Name**: `example_04_selective_test`

**Expected in Backend**:
```json
{
  "metric_name": "example_04_selective_test",
  "value": 1,
  "type": "counter",
  "resource_attributes": {
    "service.name": "example-04-selective",
    "service.version": "1.0.0"
  },
  "attributes": {}
}
```

**Verify**:
- ✓ Metric appears within 60 seconds
- ✓ Service name is "example-04-selective"
- ✓ Only metrics and traces were initialized (no logs)

---

#### Example 5: Complete Initialization

**Metric Name**: `example_05_complete_test`

**Expected in Backend**:
```json
{
  "metric_name": "example_05_complete_test",
  "value": 1,
  "type": "counter",
  "resource_attributes": {
    "service.name": "example-05-complete",
    "service.version": "1.0.0",
    "platform": "conda",
    "environment": "development",
    "parameters": "{\"example\": \"complete_initialization\", \"test_type\": \"e2e-qa\"}"
  },
  "attributes": {}
}
```

**Verify**:
- ✓ Metric appears within 60 seconds
- ✓ Service name is "example-05-complete"
- ✓ Platform is "conda"
- ✓ Environment is "development"
- ✓ Custom parameters are present in JSON format

---

#### Example 6: Environment-Based Initialization

**Metric Name**: `example_06_env_based_test`

**Expected in Backend**:
```json
{
  "metric_name": "example_06_env_based_test",
  "value": 1,
  "type": "counter",
  "resource_attributes": {
    "service.name": "example-06-env-based",
    "service.version": "1.0.0",
    "environment": "staging",
    "parameters": "{\"otel_environment\": \"staging-internal\", \"test_type\": \"e2e-qa\"}"
  },
  "attributes": {
    "environment": "staging-internal"
  }
}
```

**Verify**:
- ✓ Metric appears within 60 seconds
- ✓ Service name is "example-06-env-based"
- ✓ Resource attribute `environment` is "staging"
- ✓ Metric attribute `environment` is "staging-internal"
- ✓ Custom parameters include `otel_environment`

**Important**: This example demonstrates the difference between:
- **Resource attributes**: `environment: "staging"` (valid enum value)
- **Metric attributes**: `environment: "staging-internal"` (custom tag)

---

## Common Validation Queries

### Query 1: Find All Test Metrics

```
metric_name IN (
  "example_01_initialization_test",
  "example_02_metrics_test",
  "example_03_default_test",
  "example_04_selective_test",
  "example_05_complete_test",
  "example_06_env_based_test"
)
AND timestamp > now() - 1h
```

**Expected Result**: 6 metrics

---

### Query 2: Find Metrics by Session ID

```
session.id = "<session-id-from-console-output>"
AND timestamp > now() - 1h
```

**Expected Result**: 6 metrics with the same session ID

---

### Query 3: Verify Service Names

```
service.name LIKE "example-%"
AND timestamp > now() - 1h
GROUP BY service.name
```

**Expected Result**: 6 unique service names:
- example-01-all-signals
- example-02-metrics-only
- example-03-default
- example-04-selective
- example-05-complete
- example-06-env-based

---

### Query 4: Check Schema Version

```
schema.version = "0.3.0"
AND service.name LIKE "example-%"
AND timestamp > now() - 1h
```

**Expected Result**: All 6 metrics should have schema version "0.3.0"

---

## Validation Checklist by Attribute

### Resource Attributes to Verify

For each metric, verify these resource attributes are present:

| Attribute | Expected | Notes |
|-----------|----------|-------|
| `service.name` | `example-XX-*` | Unique per example |
| `service.version` | `1.0.0` | All examples |
| `telemetry.sdk.language` | `python` | Auto-added by SDK |
| `telemetry.sdk.name` | `opentelemetry` | Auto-added by SDK |
| `telemetry.sdk.version` | `1.38.0` | OpenTelemetry version |
| `os.type` | `Darwin`/`Linux`/`Windows` | Auto-detected |
| `os.version` | System version | Auto-detected |
| `python.version` | `3.x.x` | Auto-detected |
| `hostname` | Machine hostname | Auto-detected |
| `client.sdk.version` | `0.0.0.devbuild` | Anaconda SDK version |
| `schema.version` | `0.3.0` | Telemetry schema version |
| `session.id` | 64-char hex hash | Unique per run |

### Metric-Specific Attributes

Only `example_06_env_based_test` should have metric attributes:

| Attribute | Value |
|-----------|-------|
| `environment` | `staging-internal` |

---

## Troubleshooting

### Issue: No Metrics Appearing

**Possible Causes**:
1. Not connected to WARP
2. Wrong endpoint configured
3. Collector is down
4. Firewall blocking connection

**Steps to Debug**:
```bash
# 1. Verify endpoint
cd tests/e2e_qa
python -c "
import sys
sys.path.insert(0, 'examples')
from config_utils import load_environment
env, endpoint, _ = load_environment()
print(f'Endpoint: {endpoint}')
"

# 2. Test connection
curl -v https://metrics.stage.anacondaconnect.com/v1/metrics

# 3. Check console output for errors
python run_all_examples.py 2>&1 | grep -i error
```

---

### Issue: Metrics Missing Attributes

**Possible Causes**:
1. SDK version mismatch
2. Attribute not set correctly
3. Backend processing issue

**Steps to Debug**:
1. Check console output JSON for complete data
2. Verify SDK version: `pip show anaconda-opentelemetry`
3. Check backend logs for parsing errors

---

### Issue: Wrong Attribute Values

**Possible Causes**:
1. Environment variable not set correctly
2. Code using wrong attribute names
3. Type conversion issues

**Steps to Debug**:
1. Check `.env` file: `cat tests/e2e_qa/.env`
2. Verify environment loading: Run config_utils test
3. Check console output for actual values sent

---

## Backend System Specific Validation

### Grafana/Prometheus

```promql
# Count metrics by service name
count by (service_name) (
  {__name__=~"example_.*_test"}
)

# Check latest values
{__name__=~"example_.*_test"}[5m]
```

### Elasticsearch/Kibana

```json
{
  "query": {
    "bool": {
      "must": [
        { "wildcard": { "metric.name": "example_*_test" }},
        { "range": { "@timestamp": { "gte": "now-1h" }}}
      ]
    }
  }
}
```

### Custom Backend API

```bash
# Example API query
curl -X POST https://your-backend-api/query \
  -H "Content-Type: application/json" \
  -d '{
    "metric_names": ["example_01_initialization_test"],
    "time_range": "1h",
    "filters": {
      "service.name": "example-01-all-signals"
    }
  }'
```

---

## Expected Timeline

| Time | Event |
|------|-------|
| T+0s | Examples start running |
| T+5s | First metric sent (example_01) |
| T+10s | All 6 metrics sent |
| T+15s | Metrics arrive at collector |
| T+30s | Metrics processed and queryable |
| T+60s | All metrics visible in backend UI |

**Note**: Times may vary based on export intervals and backend processing delays.

---

## Success Criteria

The E2E QA examples are considered successful when:

✅ **All 6 metrics are visible** in the backend within 60 seconds

✅ **All resource attributes are present** and correctly formatted

✅ **Session ID is consistent** across all metrics from the same run

✅ **Timestamps are accurate** and within the expected time range

✅ **No errors** in collector or backend logs

✅ **Metric values are correct** (all should be 1)

✅ **Service names are unique** and match expected patterns

✅ **Schema version is correct** (0.3.0)

---

## Next Steps After Validation

Once backend validation is complete:

1. **Document Results**: Record what was verified and any issues found
2. **Update Examples**: Fix any issues discovered during validation
3. **Proceed to Next Phase**: Implement Phase 5 (Logging examples)
4. **Share Findings**: Communicate validation results with team

---

## Related Documentation

- **[03_implementation_plan.md](03_implementation_plan.md)** - Implementation phases and progress
- **[07_environment_configuration.md](07_environment_configuration.md)** - Environment setup and endpoint details
- **[README.md](../README.md)** - Quick start guide

---

**Questions or Issues?**

If metrics are not appearing as expected:
1. Check the troubleshooting section above
2. Verify WARP connection
3. Review console output for errors
4. Check backend system status
5. Contact the observability team for backend access issues

---

**Last Updated**: 2026-01-16  
**Validated Against**: SDK version 0.0.0.devbuild, Schema version 0.3.0
