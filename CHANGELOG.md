# CHANGELOG

We [keep a changelog.](http://keepachangelog.com/)


## [v1.0.0] (2026-01-21) - v1 Release

### !!! Breaking Changes !!!

- Updated module structure to use package nesting for consistency with other conda packages
- Now imported as `anaconda.opentelemetry` rather than `anaconda_opentelemetry`
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

### Security

- N/A

### Tickets Closed

- N/A

### Pull Requests Merged

- use package nesting for anaconda.opentelemetry [#36](https://github.com/anaconda/anaconda-otel-python/pull/36)
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
