# Private OpenTelemetry API surface

`anaconda-opentelemetry` depends on OpenTelemetry symbols that upstream does not
consider public. OpenTelemetry Python's `CONTRIBUTING.md` guarantees backwards
compatibility only for non-underscore-prefixed symbols; anything with a leading
underscore in its module path or name may change in a **minor or patch** release.

This is the reason the dependency range in `pyproject.toml` and
`conda-recipe/meta.yaml` is hard-capped (`>=1.40.0,<1.44`) rather than open-ended.
This document is the checklist to re-run before raising that cap.

Supported range: **1.40.0 – 1.43.x**. Tested points: **1.40.0** and **1.43.0**
(the only versions of the full OTel set available on the conda `defaults`
channel — see the README policy section).

All private imports are funnelled through
[`anaconda_opentelemetry/_compat.py`](../anaconda_opentelemetry/_compat.py). No
other module in the package may import a private OTel symbol directly. That file
is the whole diff for a ceiling bump.

## How to re-verify

```bash
# 1. private-API import sites; should only ever list _compat.py
grep -rn "opentelemetry\.sdk\._logs\|opentelemetry\._logs\|semconv\._incubating\|opentelemetry\..*\._internal" anaconda_opentelemetry/*.py
grep -rn "from opentelemetry\..*import .*\b_" anaconda_opentelemetry/*.py

# 2. every direct import is declared
pytest tests/integration_tests/direct_imports_test.py tests/integration_tests/dependency_sync_test.py

# 3. run the suite at the floor and the ceiling
for v in 1.40.0 1.43.0; do
  uv pip install "opentelemetry-sdk==$v" "opentelemetry-api==$v" \
    "opentelemetry-exporter-otlp-proto-common==$v" \
    "opentelemetry-exporter-otlp-proto-grpc==$v" \
    "opentelemetry-exporter-otlp-proto-http==$v"
  OTEL_USE_CONSOLE_EXPORTER=TRUE pytest tests
done
```

## Inventory

| Symbol | Module | Why private | Status across 1.40.0 – 1.43.0 | What breaks outside the range |
|---|---|---|---|---|
| `set_logger_provider`, `get_logger_provider`, `Logger`, `LoggerProvider` (API) | `opentelemetry._logs` | Whole module is underscore-prefixed: the OTel **logs signal is not stable**, so the API package keeps it out of the public namespace. | Unchanged. | The logs API is expected to be promoted to `opentelemetry.logs` when the signal stabilises. At that point `opentelemetry._logs` may be removed and log telemetry stops initialising. |
| `Logger`, `LoggerProvider`, `LoggingHandler` | `opentelemetry.sdk._logs` | Same: unstable logs signal. | Present in both. `LoggerProvider.__init__` gained keyword-only `meter_provider=` and `_logger_configurator=` in 1.43 (additive; we do not pass them). `LoggingHandler.__init__(level, logger_provider)` identical. | Removal/rename of the module breaks `_AnacondaLogger` construction and the stdlib logging bridge. |
| `Logger.emit(...)` keyword form | `opentelemetry.sdk._logs` | Same. | `emit(record=None, *, timestamp, observed_timestamp, context, severity_number, severity_text, body, attributes, event_name)` in 1.40; 1.43 adds keyword-only `exception=`. Purely additive. | **< 1.39.0**: `emit()` took a single positional `LogRecord` and the keyword form did not exist. Flooring at 1.40.0 removes the need for that branch; the previous shape-detection code has been deleted. |
| `ReadableLogRecord` / `ReadWriteLogRecord` | `opentelemetry.sdk._logs` | Same. | Present in 1.40 and 1.43. `LogRecord` is **absent** from `opentelemetry.sdk._logs` in both. | **< 1.39.0**: these names do not exist; the type was `LogRecord`. Renamed by [open-telemetry/opentelemetry-python#4676](https://github.com/open-telemetry/opentelemetry-python/pull/4676) in 1.39.0. A floor of 1.37/1.38 would straddle this rename and require dual-path imports. A floor of 1.40.0 sits entirely on the post-rename side — this is the primary justification for 1.40.0. |
| `LogRecordExporter` (and deprecated alias `LogExporter`) | `opentelemetry.sdk._logs.export` | Same. | Both names present in 1.40 and 1.43; `LogExporter` is a deprecated subclass that emits a `DeprecationWarning` on subclassing. `OTLPLogExporterShim` subclasses `LogRecordExporter`. `export(batch: Sequence[ReadableLogRecord])` identical. | `LogExporter` is scheduled for removal; using `LogRecordExporter` is forward-safe within the range. Below 1.39 only `LogExporter` exists. |
| `BatchLogRecordProcessor`, `ConsoleLogRecordExporter` (alias `ConsoleLogExporter`) | `opentelemetry.sdk._logs.export` | Same. | Present in both. `BatchLogRecordProcessor.__init__` gained keyword-only `meter_provider=` in 1.43 (additive). `ConsoleLogRecordExporter(out, formatter)` identical; its `out` attribute is mutated by `_test_set_console_mock`. | Rename or removal breaks log batching and the console-exporter test hook. |
| `OTLPLogExporter` | `opentelemetry.exporter.otlp.proto.grpc._log_exporter`, `opentelemetry.exporter.otlp.proto.http._log_exporter` | Module is underscore-prefixed because the logs exporter tracks the unstable logs signal. Upstream has never published a public path for it. | Present in both. 1.43 adds `retryable_error_codes=` (gRPC) and keyword-only `meter_provider=` (both). All arguments we pass (`endpoint`, `insecure`, `credentials`, `headers`, `timeout`, `certificate_file`, `client_key_file`, `client_certificate_file`) are unchanged. | Rename of `_log_exporter` breaks OTLP log export; imports are lazy (inside `_AnacondaLogger.__init__`) so failure surfaces at initialisation, not import. |
| `_Gauge` | `opentelemetry.sdk.metrics` | Underscore-prefixed because the synchronous gauge instrument is newer than the metrics stability freeze; there is still **no** public `opentelemetry.sdk.metrics.Gauge` or `opentelemetry.metrics.Gauge` in 1.43. | Present in both, aliasing `opentelemetry.sdk.metrics._internal.instrument.Gauge`. Used only as a dict key in the temporality maps. | If renamed to a public `Gauge`, the temporality maps silently lose their gauge entry and gauges fall back to the reader default. `_compat` resolves the public name first and falls back to `_Gauge`, so a future rename is absorbed. |

### Not declared as dependencies

The declared set is deliberately equal to the **imported** set. Verified by a
hardcoded list in `tests/integration_tests/direct_imports_test.py`. What we declare:
`opentelemetry-api`, `opentelemetry-sdk`,
`opentelemetry-exporter-otlp-proto-grpc`, `opentelemetry-exporter-otlp-proto-http`,
plus `grpcio` and `requests`.

Three OTel packages get installed but are **not** declared, for two different
reasons:

- `opentelemetry-semantic-conventions` — **the dangerous one.** Not imported
  anywhere (the `ResourceAttributes` class in this package is its own, defined in
  `attributes.py`; it is not the semconv one). It is versioned off the main train:
  0.61b0 pairs with 1.40, 0.64b0 with 1.43. So the stale `==0.61b0` that used to be
  declared here would, against a widened SDK range, be satisfied by resolving the
  SDK back *down* to 1.40.0 — silently, with no error and no warning. Verified:
  with semconv undeclared, solving the range from `defaults` correctly trains it to
  0.61b0 at OTel 1.40.0 and 0.64b0 at 1.43.0.
- `opentelemetry-exporter-otlp-proto-common` and `opentelemetry-proto` — merely
  **redundant.** Neither is imported, and both are pinned `==<exact>` by the
  exporters we do declare:

  ```
  exporter-otlp-proto-{grpc,http}  ==>  exporter-otlp-proto-common == <exact>
                                        opentelemetry-proto        == <exact>
  exporter-otlp-proto-common       ==>  opentelemetry-proto        == <exact>
  ```

  That exact pin dominates any range we could write, so declaring them would
  document the dependency tree rather than constrain anything. Note this also means
  a range on either is *harmless* — unlike semconv, they cannot cause the
  silent-downgrade above. They are omitted to keep one rule ("declare what you
  import") rather than a partial mirror of the tree.

The `defaults` **availability** check in `tests/integration_tests/defaults_availability_test.py` is
deliberately broader than the declared set: it intersects all six OTel packages,
because a missing `defaults` build of, say, `opentelemetry-proto` makes a version
uninstallable no matter what our own metadata says.

### Depended on directly, and easy to miss

- `grpcio` — `config.py` does `import re, os, grpc, warnings, functools` at module
  level and calls `grpc.ssl_channel_credentials()`. The shared import line means a
  search for `import grpc` does **not** match it, which makes `grpcio` look like a
  transitive of `opentelemetry-exporter-otlp-proto-grpc` when it is not.
  `tests/integration_tests/direct_imports_test.py` exists to catch exactly this. The
  `>=1.71.0` floor is kept: the exporter's own floor is `>=1.63.2` (`>=1.66.2` on
  py3.13, `>=1.75.1` on py3.14), but the lowest grpcio at or above that on
  `defaults` is 1.71.0 anyway, so this floor costs nothing there.
- `requests` — imported lazily in `config.py` only when a proxy is configured.
  Declared with `>=2.32.5`; satisfied in practice by
  `opentelemetry-exporter-otlp-proto-http`, which requires it.
- `anaconda_anon_usage` — optional, guarded by `try`/`except` in `attributes.py`.
  Declared in `conda-recipe/meta.yaml` `run:` only, since it is a conda-only
  package.

### Failure mode

`_compat.py` wraps every private import in a single `try`/`except Exception`. If
any of them fails, the module logs **one** warning and exports no-op stand-ins,
so a private-API break degrades log telemetry to a no-op rather than raising out
of a log handler and taking down the host application. `signals.py` checks
`_compat.OTEL_PRIVATE_LOGS_AVAILABLE` before enabling the logging signal.
