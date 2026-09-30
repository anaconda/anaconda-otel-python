# CHANGELOG

We [keep a changelog.](http://keepachangelog.com/)

## [v1.3.0]

### Added

- Support for a range of OpenTelemetry versions (**1.40.0 – 1.43.x**) instead of a single exact pin. The tested set is 1.40.0 and 1.43.0, which are the only versions of the full OTel package set carried by the conda `defaults` channel
- `anaconda_opentelemetry/_compat.py`: every private OpenTelemetry import is now funnelled through one module, so a version bump is a one-file diff instead of a repository-wide audit. A broken private import now degrades log telemetry to a no-op with a single warning rather than raising out of a log handler
- `docs/source/otel-private-api.md`: written inventory of the private OTel API surface this package depends on, with the version range each symbol is valid in
- README section documenting the OpenTelemetry version support policy
- `tests/unit_tests/dependency_sync_test.py`: asserts the OTel, `grpcio` and `pyyaml` ranges in `pyproject.toml` and `conda-recipe/meta.yaml` match, normalizing conda's `<X.Y.0a0` pre-release spelling against pip's `<X.Y`
- `tests/unit_tests/direct_imports_test.py`: AST-walks the package and asserts every directly-imported third-party distribution is declared. A grep for `import grpc` does not match `import re, os, grpc, warnings` in `config.py`, which makes `grpcio` look like a droppable transitive dependency when it is not
- `tests/unit_tests/defaults_availability_test.py`: availability-drift check that fails when `defaults` publishes an OTel version inside our range that CI does not test, when `defaults` reaches our ceiling, or when a minor series reachable from PyPI inside our range is absent from both CI matrices
- `.github/workflows/otel-deps-test.yaml`: runs the availability-drift check on every PR to `main`. It reads live channel contents, so it can begin failing because a third party published a release rather than because of the diff — which is the signal to open a ceiling-ratchet PR
- `.github/actions/pypi-package-tests/action.yaml` and a `pypi-package-tests` matrix: covers the PyPI channel, which `defaults` cannot represent. Pip can resolve 1.41.x and 1.42.x from the continuous declared range, and `defaults` carries neither. Pins are passed to the same `pip install` as the built wheel, so an out-of-range pin is a resolution error. One unpinned cell per end of `requires-python` gives pip a free solve of `pyproject.toml` — the only place in CI where the declared dependency block reaches a resolver, since the conda path installs from `meta.yaml`
- `test:` section in the conda recipe that imports the built package

### Changed

- **Dependency ranges widened** in both `pyproject.toml` and `conda-recipe/meta.yaml`: `opentelemetry-api`, `opentelemetry-sdk`, `opentelemetry-exporter-otlp-proto-grpc` and `opentelemetry-exporter-otlp-proto-http` are now `>=1.40.0,<1.44`
- **Declared set reduced to the imported set.** `opentelemetry-proto`, `opentelemetry-exporter-otlp-proto-common` and `opentelemetry-semantic-conventions` are no longer declared in either file: this package imports none of them, and the exporters it does declare pin all three `==<exact>`. The stale `opentelemetry-semantic-conventions==0.61b0` was the hazard — because semconv is versioned off the main train (`0.61b0` pairs with 1.40, `0.64b0` with 1.43), it would have been satisfied by silently resolving the SDK back down to 1.40.0
- PR CI now runs the conda package tests as a version matrix: the ceiling (1.43) on every supported Python, plus the floor (1.40) on the newest Python. Test environments are solved with `--override-channels -c defaults`, so a range that cannot be satisfied from `defaults` now fails in CI rather than in a user's environment
- Lint and type checks moved to a single dedicated job instead of running on every matrix cell
- `OTLPLogExporterShim` now subclasses `LogRecordExporter` rather than the deprecated `LogExporter` alias, removing a `DeprecationWarning`
- `conda-recipe/meta.yaml` `host:` now mirrors the `python >=3.10` floor from `run:`

### Deprecated

- N/A

### Removed

- `opentelemetry-semantic-conventions` and `opentelemetry-proto` are no longer declared as direct dependencies. The package imports neither, and the SDK and exporters already pin both exactly. Keeping the stale `opentelemetry-semantic-conventions ==0.61b0` pin alongside a widened SDK range would have silently resolved the SDK back down to 1.40.0 with no error and no warning. `grpcio >=1.71.0` is retained: `config.py` imports `grpc` at module level
- Runtime shape-detection for `Logger.emit` and the `opentelemetry.sdk._logs.LogRecord` import fallback. The 1.40.0 floor sits entirely on the post-1.39 side of the `ReadableLogRecord` / `ReadWriteLogRecord` rename, so neither branch is reachable

### Fixed

- N/A

### Security

- N/A

### Tickets Closed

- CASH-3728

### Pull Requests Merged

- N/A

## [v1.2.5]

### Added

- N/A

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- `flush_telemetry` now behaves as expected when there are multiple instantiated LoggerProviders in a process

### Security

- N/A

### Tickets Closed

- N/A

### Pull Requests Merged

- Support flush of anaconda-opentelemetry given multiple LoggerProviders [#100](https://github.com/anaconda/anaconda-otel-python/pull/100)

## [v1.2.4]

### Added

- Allows user to opt out of `ATEL_*` and `OTEL_SDK_DISABLED` environment variables effecting the `Configuration`

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- N/A

### Security

- N/A

### Tickets Closed

- N/A

### Pull Requests Merged

- feat: Optional config flag ignores env vars [#98](https://github.com/anaconda/anaconda-otel-python/pull/98)


## [v1.2.3]

### Added

- Allows user to opt out of all auto collected resource attributes
- Allows user to opt out of specific auto collected resource attributes

### Changed

- Updated export schema to v0.5.0 - optional auto collected attributes

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- N/A

### Security

- N/A

### Tickets Closed

- N/A

### Pull Requests Merged

- feat: Allow for opt out of automatically collected attributes [#97](https://github.com/anaconda/anaconda-otel-python/pull/97)


## [v1.2.2]

### Added

- Added the `gauge` metric type and the `set_gauge` API for recording last-value metrics
- Automatic hashing for hostname telemetry attribute

### Changed

- OpenTelemetry SDK logs are now suppressed by default to support CLI implementation, use `set_verbose_export_errors(True)` to enable those logs (more detail in `getting_started.md`)
- Updated telemetry attributes to serialize list and dict objects
- Allow metric name regex to accept . characters
- Updated opentelemetry dependencies to v1.40.0
- Various attribute logs changes from error to debug

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- Entire attributes payload is no longer discarded if an attributes has a key equal to `None`
- `_process_attributes` no longer mutates the passed attribute dict

### Security

- N/A

### Tickets Closed

- N/A

### Pull Requests Merged

- Added gauge + tests, fixed failing test [#91](https://github.com/anaconda/anaconda-otel-python/pull/91)
- Support . chars in metric names [#84](https://github.com/anaconda/anaconda-otel-python/pull/84)
- Support list and tuple types as telemetry attributes [#92](https://github.com/anaconda/anaconda-otel-python/pull/92)
- fix: Make None attribute key only drop itself [#93](https://github.com/anaconda/anaconda-otel-python/pull/93)
- fix: hash hostname by default [#94](https://github.com/anaconda/anaconda-otel-python/pull/94)
- fix: hostname hash not consistent between signal types [#95](https://github.com/anaconda/anaconda-otel-python/pull/95)


## [v1.2.1] (2026-07-08)

### Added

- Added `send_event` to `__init__.py`

### Changed

- Updated `shutdown_telemetry` docstring to reflect actual setup

### Deprecated

- N/A

### Removed

- Log warnings for `None` resource attribute values if the key stems from `anaconda-anon-usage`

### Fixed

- Fixes different import path required by exclusion of send_event

### Security

- N/A

### Tickets Closed

- N/A

### Pull Requests Merged
- pip install reads version [#71](https://github.com/anaconda/anaconda-otel-python/pull/71)



## [v1.2.0] (2026-06-09)

### Added

- Added `shutdown_on_exit` to `Configuration` which allows consumers to toggle the OpenTelemetry behavior on process exit

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- Issue with shutdown that caused OpenTelemetry exporters to hang in certain conditions
- Pip now can read the package version

### Security

- N/A

### Tickets Closed

- N/A

### Pull Requests Merged
- pip install reads version [#66](https://github.com/anaconda/anaconda-otel-python/pull/66)
- allow consumers to manage shutdown [#69](https://github.com/anaconda/anaconda-otel-python/pull/69)



## [v1.1.0] (2026-04-17)

### Added

- Added EventLogger - simple python event logger for log structured data that does not qualify as developer logging
- Native OIDC authenticator support
- Proxy support for exporters (exporter session respects proxy)
- anaconda-anon-usage token integration via anaconda-anon-usage dependency for telemetry attributes

### Changed
- Added processing for EventLogger to handle string payloads and JSON
- File structure of some signal modules. No impact to usage

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- Fixed LogRecord usage which was causing ResourceAttributes to be omitted from EventLogger logs

### Security

- N/A

### Tickets Closed

- N/A

### Pull Requests Merged
- EventLogger Implementation [#47](https://github.com/anaconda/anaconda-otel-python/pull/47)
- process JSON in EventLogger [#48](https://github.com/anaconda/anaconda-otel-python/pull/48)
- Reorganize files [#49](https://github.com/anaconda/anaconda-otel-python/pull/49)
- Native OIDC Authenticator [#51](https://github.com/anaconda/anaconda-otel-python/pull/51)
- [feat] Proxy support for exporters [#54](https://github.com/anaconda/anaconda-otel-python/pull/54)
- [fix] service.name resource attribute lost during log event emission [#58](https://github.com/anaconda/anaconda-otel-python/pull/58)
- [feat] Add anon-usage information to telemetry attributes [#62](https://github.com/anaconda/anaconda-otel-python/pull/62)

## [v1.0.1] (2026-02-04)

### Added

- N/A

### Changed
- Removed package namespacing added in v1.0.0
- Returns to `anaconda_opentelemetry`

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- N/A

### Security

- N/A

### Tickets Closed

- N/A

### Pull Requests Merged
- [fix] revert package namespacing [#45](https://github.com/anaconda/anaconda-otel-python/pull/45)



## [v1.0.0] (2026-02-03) - v1 Release

### !!! Breaking Changes !!!

- Updated module structure to use package nesting for consistency with other conda packages
- Now imported as `anaconda_opentelemetry` rather than `anaconda_opentelemetry`
- Documentation has been updated to reflect this

### Added

- Exporter shim that allows for reconfiguration of export parameters (endpoint, token, etc.) during runtime
- Metric exports now default to delta aggregation temporality, `set_use_cumulative_metrics` config function toggles this
- More reliable attribute payload casting, now uses json.dumps
- More detailed exceptions when telemetry is not initialized
- Added carrier injection to complete context aware span collection
- Added configurable interval to trace export, `set_tracing_export_interval_ms` config function handles this
- Documentation is hosted at https://anaconda.github.io/anaconda-otel-python/docs/index.html
- Added documentation addressing best practices and tradeoffs between metrics/traces/logs

### Changed

- Improved endpoint configuration by condensing required calls
- Improved documentation detail
- Added and improved test cases
- Changed user.id attribute to default to being event dependent
- Changed schema version from `v0.2.0` to `v0.3.0` in [#26](https://github.com/anaconda/anaconda-otel-python/pull/26)

### Deprecated

- `set_auth_token`
- `set_auth_token_logging`
- `set_auth_token_tracing`
- `set_auth_token_metrics`
- `set_tls_private_ca_cert`
- `set_tls_private_ca_cert_logging`
- `set_tls_private_ca_cert_tracing`
- `set_tls_private_ca_cert_metrics`

### Removed

- N/A

### Fixed

- Vague exception handling for cases where telemetry is not initialized
- Changed string casting of json objects to json.dumps
- Fix counter (cumulative) not being DELTA temporality
- Added more endpoint validation, fixed bug where user could create an empty string endpoint

### Security

- N/A

### Tickets Closed

- N/A

### Pull Requests Merged

- Generalizing schema, added endpoint guidance [#44](https://github.com/anaconda/anaconda-otel-python/pull/44)
- [fix] Corrected fix for endpoint validation [#43](https://github.com/anaconda/anaconda-otel-python/pull/43)
- Lower maximum service name characters [#41](https://github.com/anaconda/anaconda-otel-python/pull/41)
- use package nesting for anaconda_opentelemetry [#36](https://github.com/anaconda/anaconda-otel-python/pull/36)
- [fix] Update Temporality presets for Metrics [#35](https://github.com/anaconda/anaconda-otel-python/pull/35)
- Add Best Practices Documentation [#34](https://github.com/anaconda/anaconda-otel-python/pull/34)
- Add publishing documentation and coverage report on PR merge. [#31](https://github.com/anaconda/anaconda-otel-python/pull/31)
- add interval to BatchSpanProcessor config [#30](https://github.com/anaconda/anaconda-otel-python/pull/30)
- [update] Update OpenTelemetry Dependencies to conda Latest (v1.38) [#27](https://github.com/anaconda/anaconda-otel-python/pull/27)
- Default to Event Dependent user.id [#26](https://github.com/anaconda/anaconda-otel-python/pull/26)
- [update] added integration test for get_trace and carrier [#21](https://github.com/anaconda/anaconda-otel-python/pull/21)
- Add Span Carrier Injection [#20](https://github.com/anaconda/anaconda-otel-python/pull/20)
- [update] Update OpenTelemetry Dependencies to conda Latest (v1.37) [#19](https://github.com/anaconda/anaconda-otel-python/pull/19)
- Exporter Shim for Export Endpoint/Token Changes During Runtime [#18](https://github.com/anaconda/anaconda-otel-python/pull/18)
- Improve Documentation and Add Examples [#17](https://github.com/anaconda/anaconda-otel-python/pull/17)
- [fix] Improve str cast [#14](https://github.com/anaconda/anaconda-otel-python/pull/14)
- [fix] Add better exception catching at the api level. [#13](https://github.com/anaconda/anaconda-otel-python/pull/13)
- Endpoint config improvements [#11](https://github.com/anaconda/anaconda-otel-python/pull/11)
- [fix] Make delta temporality the default, cumulative aggregation optionally. [#10](https://github.com/anaconda/anaconda-otel-python/pull/10)



## [v0.8.1] (2025-08-12) - [Bug Fix] Beta 2 Release

### Added

- N/A

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- N/A

### Security

- N/A

### Tickets Closed

- N/A

### Pull Requests Merged

- N/A
