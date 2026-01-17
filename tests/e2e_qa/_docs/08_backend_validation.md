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

### Critical Configuration

**⚠️ Console Exporter MUST Be Disabled for Backend Validation**

Console exporter and remote backend are **mutually exclusive**:
- `OTEL_CONSOLE_EXPORTER=true` → Data goes to console ONLY (not backend)
- `OTEL_CONSOLE_EXPORTER=false` → Data goes to backend ONLY (not console)

**Required `.env` configuration**:
```bash
OTEL_CONSOLE_EXPORTER=false  # CRITICAL!
OTEL_ENVIRONMENT=staging-internal
```

### Other Prerequisites

- Examples have been run successfully (see `run_all_examples.py`)
- Access to staging backend/observability tools
- WARP VPN connection active
- Note the session ID from the console output for filtering
- Flush must be called (examples do this automatically)

## Quick Start - Step by Step

### Step 1: Configure for Backend

```bash
cd tests/e2e_qa

# Edit .env file
cat > .env << 'EOF'
OTEL_ENVIRONMENT=staging-internal
OTEL_CONSOLE_EXPORTER=false
EOF
```

### Step 2: Run Examples

```bash
python run_all_examples.py
```

**Expected Output** (no JSON because console exporter is disabled):
```
✓ All initialization examples completed!
  Flushing all telemetry data to backend...
✓ All telemetry data flushed to backend

📋 BACKEND VALIDATION SUMMARY
======================================================================

📊 Metrics Sent:
   1. example_01_initialization_test (service: example-01-all-signals)
   2. example_02_metrics_test (service: example-02-metrics-only)
   3. example_03_default_test (service: example-03-default)
   4. example_04_selective_test (service: example-04-selective)
   5. example_05_complete_test (service: example-05-complete)
   6. example_06_env_based_test (service: example-06-env-based)
```

### Step 3: Wait and Query

Wait 1-2 minutes for backend processing, then query using the SQL examples below.

---

## Quick Verification Checklist

Use this checklist for a quick validation:

- [ ] Set `OTEL_CONSOLE_EXPORTER=false` in `.env`
- [ ] Verify WARP VPN is connected
- [ ] Run examples and verify flush message appears
- [ ] Wait 1-2 minutes for backend processing
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

**File**: `run_initialization_examples.py` (runs individual scripts)

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

## Common Validation Scenarios

### Scenario 1: Validate All Initialization Examples in Backend

```bash
cd tests/e2e_qa
python run_initialization_examples.py
```

Wait 1-5 minutes, then query backend for 6 services.

---

### Scenario 2: Test One Specific Initialization Pattern

```bash
cd tests/e2e_qa
python examples/01_all_signals.py
```

Wait 1-5 minutes, then query backend for `example-01-all-signals`.

---

### Scenario 3: Demo All SDK Functionality

```bash
cd tests/e2e_qa
python run_all_examples.py
```

Shows config, attributes, and initialization examples. Backend will have 6 records from initialization examples.

---

### Scenario 4: Test Configuration Options (No Backend)

```bash
cd tests/e2e_qa
python examples/01_config_examples.py
```

No backend data sent (just demonstrates configuration API).

---

## Validation Query: Snowflake Backend Query (Recommended - Use Explicit Timestamp)
[Confluence article - how to work with Snowflake DB](https://anaconda.atlassian.net/wiki/spaces/QA/pages/5105221635/QA+Telemetry+with+OpenTelemetry)

```sql
SELECT 
  f.value:value:stringValue::string as service_name,
  m.data:resourceMetrics[0]:scopeMetrics[0]:metrics[0]:name::string as metric_name,
  m.LOAD_TIMESTAMP_UTC,
  m.data:resourceMetrics[0]:resource:attributes as resource_attributes
FROM raw.otel.metrics m,
     LATERAL FLATTEN(input => m.data:resourceMetrics[0]:resource:attributes) f
WHERE m.LOAD_TIMESTAMP_UTC > '2026-01-17 03:00:00'  -- Replace with your desired UTC timestamp
  AND f.value:key::string = 'service.name'
  AND f.value:value:stringValue::string LIKE 'example-%'
ORDER BY m.LOAD_TIMESTAMP_UTC DESC
LIMIT 1000;
```

**Expected Result**: 6 rows (1 record per one example, after running `run_initialization_examples.py` or `run_all_examples.py`)


## Validation Checklist by Attribute

### Resource Attributes to Verify

For each metric, verify these resource attributes are present: compare data in DB and from console

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

## Validation Modes

### Mode 1: Local Debugging (Console Only)

```bash
# .env
OTEL_CONSOLE_EXPORTER=true
```

**Use for**: Seeing telemetry data structure, debugging locally  
**Result**: JSON printed to console, **no backend data**

### Mode 2: Backend Validation (Remote Only)

```bash
# .env
OTEL_CONSOLE_EXPORTER=false
```

**Use for**: Validating data reaches backend  
**Result**: No console output, **data sent to backend**

### Mode 3: Both (Not Supported)

Currently not supported by SDK. You must choose one or the other.

**Workaround**: Run twice with different settings:
```bash
# First run: Debug locally
OTEL_CONSOLE_EXPORTER=true python run_all_examples.py > local_output.txt

# Second run: Send to backend
OTEL_CONSOLE_EXPORTER=false python run_all_examples.py
```

---

## Troubleshooting

### Issue: No Metrics Appearing

**Check 1: Console Exporter Setting**
```bash
grep OTEL_CONSOLE_EXPORTER .env
# Should show: OTEL_CONSOLE_EXPORTER=false
```

**This is the most common issue!** If console exporter is enabled, data will NOT go to backend.

**Check 2: WARP Connection**
```bash
# Verify WARP is connected (required for staging-internal)
# Check WARP status in menu bar or system tray
```

**Check 3: Flush Was Called**
```bash
# Run examples and check output
python run_all_examples.py | grep "flushed"
# Should show: "✓ All telemetry data flushed to backend"
```

**Check 4: Endpoint Connectivity**
```bash
# Test if endpoint is reachable
curl -v https://metrics.stage.anacondaconnect.com/v1/metrics
```

**Check 5: Verify Endpoint Configuration**
```bash
cd tests/e2e_qa
python -c "
import sys
sys.path.insert(0, 'examples')
from config_utils import load_environment
env, endpoint, _ = load_environment()
print(f'Endpoint: {endpoint}')
"
```

---

### Issue: "No JSON output"

**This is CORRECT when `OTEL_CONSOLE_EXPORTER=false`**

The console exporter and remote backend are mutually exclusive:
- Console exporter ON → See JSON in console, nothing in backend
- Console exporter OFF → No JSON in console, data goes to backend

---

### Issue: "Connection refused" or "Timeout"

**Solutions**:
1. Check WARP VPN is connected
2. Verify endpoint URL is correct
3. Check firewall settings
4. Try internal endpoint: `https://metrics.stage.internal.anacondaconnect.com/v1/metrics`

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

## Success Criteria

The E2E QA examples are considered successful when:

✅ **All 6 metrics are visible** in the backend within XX seconds

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
