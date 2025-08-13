# CHANGELOG

We [keep a changelog.](http://keepachangelog.com/)

## [v0.8.1] (2025-08-12) - [Bug Fix] Beta 2 Release

### Added

- N/A

### Changed

- Documentation updates
- Code comment and function doc string updates

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- Bug where a non-existent method was called during span generation
- Now recording actual histogram values instead of timestamps

### Security

- N/A

### Tickets Closed

- N/A

### Pull Requests Merged

- PR# 88 [Fix] Code using removed method.
- PR# 95 backstage documentation improvements
- PR# 101 [Fix] record actual histogram value instead of timestamp. 

## [v0.8.0] (2025-07-17) - Beta 2 Release

### Added

- v0.8.0 Configuration class now supports configuration of different export protocols, authorization, and certificates for each signal.

### Changed

- v0.8.0 Upon export of telemetry, various ResourceAttributes will have their keys change to fit standard OpenTelemetry conventions. This does not effect clientside instrumentation, however.
- v0.8.0 Documentation reviewed and updated.

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

- PR# 77 updating class docstring to have clearer function
- PR# 74 Update Schema
- PR# 71 Rework config
- PR# 70 Fix docs for protocol support
- PR# 69 [Fix] package name is wrong in quickstart guide.

## [v0.5.0] (2025-07-01) - Beta 1 Release

### Added

- v0.5.0 In Configuration, added a property to skip the internet check for on-prem (no internet access) installs.

### Changed

- v0.5.0 Seperated the Configuration class into its own python file.
- v0.5.0 All Configuration values now have environment variables using predictable names (see documentation).
- v0.5.0 A logging handler for signals is no longer injected, instead the package user can get the handler and use it in their named logger.
- v0.5.0 Separate start and end trace events are no longer sent, this is implied by the span and is unneccessary.
- v0.5.0 Documentation reviewed and updated.
- v0.5.0 Now supporting HTTP exporter usage in the Configuration
- v0.5.0 OpenTelemetry api paths are now automatically appended to each signal endpoint if the user does not include them

### Deprecated

- N/A

### Removed

- v0.5.0 ASpan (returned from _get_trace_) no longer has public properties.
- v0.5.0 ASpan (returned from _get_trace_) no longer has a _set\_ok\_status_ function, OK is the default.
- v0.5.0

### Fixed

- N/A

### Security

- N/A

### Tickets Closed

- N/A

### Pull Requests Merged

- PR# 61 Add endpoint paths
- PR# 60 Add parameters attribute
- PR# 59 [Cleanup,Fix] Removed unused configuration flag and doc fixes.
- PR# 58 More doc cleanup
- PR# 56 Support http
- PR# 55 [Fix] Changed Tracing, fixed logger bug, renamed double-underscores
- PR# 54 [Fix] Change/simplify logging setup to be more Python standard.
- PR# 52 [Fix] Generalizer environment variables and replace OTEL_ with ATEL_.
- PR# 53 Add tests ensuring valid export operations for all signals
- PR# 51 Feature/HUB-2017 docs updates
- PR# 50 [feat] Now support http[s] urls for gRPC. Do not support real http OTLP.
- PR# 49 [alpha-review-fix] Fixed possible unintended 4 sec pause, and other cleanup
- PR# 47 use api path, fix build.sh


## [v0.1.0] (2025-06-13) - Pre-Alpha Release for Review

### Added

- CHANGELOG.md added to root project to track features and bug fixes pertaining to each version.

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

### Tickets closed

- [HUB-1930](https://anaconda.atlassian.net/browse/HUB-1930) - Changelog and Release Guide

### Pull Requests Merged

- [Adding changelog to manage pull requests and releases](https://github.com/anaconda/anaconda-opentelemetry/pull/44)
