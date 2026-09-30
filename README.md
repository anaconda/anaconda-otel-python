# anaconda/anaconda-otel-python
![License](https://img.shields.io/github/license/anaconda/anaconda-otel-ts)
[![Types](https://img.shields.io/badge/types-Python-blue)](#)

## About
This project wraps the Open Telemetry Python SDK to make it's usage simpler for developers.

## Getting Started and API Documentation
The API documentation can be found [here](https://anaconda.github.io/anaconda-otel-python/docs/index.html). This
includes a quickstart guide accessed from the left list.

The OpenTelemetry output format is documented at [this location](https://github.com/anaconda/anaconda-otel-python/blob/main/docs/source/schema-versions.md).

## Requirements
- python >= 3.10

## OpenTelemetry version support

| | |
|---|---|
| **Supported range** | `opentelemetry-* >= 1.40.0, < 1.44` (i.e. 1.40.0 through 1.43.x) |
| **Tested in CI** | **1.40.0** and **1.43.0** |
| **Ceiling policy** | raised one minor at a time, in a dedicated PR, after the matrix passes |

## Coverage Report
The latest coverage report for the last merged Pull Request is [here](https://anaconda.github.io/anaconda-otel-python/coverage/index.html).

## Changelog
See [CHANGELOG.md](./CHANGELOG.md) for full version history.
