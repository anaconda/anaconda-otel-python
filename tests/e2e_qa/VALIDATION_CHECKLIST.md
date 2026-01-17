# Backend Validation Quick Checklist

**Quick reference for validating E2E QA examples in staging backend**

## Step 1: Run Examples

```bash
cd tests/e2e_qa
python run_all_examples.py
```

**Note the Session ID** from console output (64-char hex hash)

---

## Step 2: Wait for Data

⏱️ Wait **60 seconds** for metrics to appear in backend

---

## Step 3: Verify Metrics

### Expected Metrics (6 total)

| # | Metric Name | Service Name | Special Attributes |
|---|-------------|--------------|-------------------|
| 1 | `example_01_initialization_test` | `example-01-all-signals` | None |
| 2 | `example_02_metrics_test` | `example-02-metrics-only` | None |
| 3 | `example_03_default_test` | `example-03-default` | None |
| 4 | `example_04_selective_test` | `example-04-selective` | None |
| 5 | `example_05_complete_test` | `example-05-complete` | platform="conda", env="development" |
| 6 | `example_06_env_based_test` | `example-06-env-based` | metric attr: environment="staging-internal" |

### Quick Query

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

**Expected**: 6 metrics

---

## Step 4: Verify Attributes

### Common Resource Attributes (All Metrics)

- [ ] `service.name` = `example-XX-*`
- [ ] `service.version` = `1.0.0`
- [ ] `telemetry.sdk.language` = `python`
- [ ] `telemetry.sdk.version` = `1.38.0`
- [ ] `os.type` = `Darwin`/`Linux`/`Windows`
- [ ] `python.version` = `3.x.x`
- [ ] `client.sdk.version` = `0.0.0.devbuild`
- [ ] `schema.version` = `0.3.0`
- [ ] `session.id` = `<64-char-hash>`

### Metric-Specific Checks

#### Example 5: Complete Test
- [ ] `platform` = `conda`
- [ ] `environment` = `development`
- [ ] `parameters` contains JSON with `example` and `test_type`

#### Example 6: Environment-Based Test
- [ ] Resource attribute `environment` = `staging`
- [ ] Metric attribute `environment` = `staging-internal`
- [ ] `parameters` contains `otel_environment`

---

## Step 5: Verify Values

All metrics should have:
- [ ] Value = `1`
- [ ] Type = `counter` (or `sum`)
- [ ] Aggregation temporality = `delta` (1) or `cumulative` (2)

---

## Step 6: Verify Session Consistency

All 6 metrics should have:
- [ ] Same `session.id`
- [ ] Timestamps within ~10 seconds of each other
- [ ] Same `hostname`

---

## Troubleshooting

### No Metrics?
1. Check WARP connection
2. Verify endpoint: `https://metrics.stage.anacondaconnect.com/v1/metrics`
3. Check console output for errors
4. Wait another 30 seconds

### Missing Attributes?
1. Check console JSON output
2. Verify SDK version
3. Check backend processing logs

### Wrong Values?
1. Verify `.env` configuration
2. Check console output matches backend
3. Review backend parsing logic

---

## Success Criteria

✅ All 6 metrics visible  
✅ All attributes present  
✅ Values correct (all = 1)  
✅ Session ID consistent  
✅ Timestamps recent  
✅ No errors in logs

---

**For detailed validation guide, see**: [_docs/08_backend_validation.md](_docs/08_backend_validation.md)
