#!/bin/bash
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

cd "$(dirname "$0")"

export OTEL_USE_CONSOLE_EXPORTER=TRUE
unset ATEL_DEFAULT_AUTH_TOKEN
unset ATEL_METRICS_AUTH_TOKEN
unset ATEL_DEFAULT_ENDPOINT
unset ATEL_METRICS_ENDPOINT

# Run tests for the anaconda_opentelemetry package.
pytest --color=yes --cov=./anaconda_opentelemetry --cov-report=html --cov-report=term tests/unit_tests

if [ $? -ne 0 ]; then
    echo
    echo ">>> FAILED"
    exit 2
else
    echo
    echo ">>> PASSED"
    exit 0
fi
