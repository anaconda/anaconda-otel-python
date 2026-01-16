#!/bin/bash
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

cd "$(dirname "$0")/.."

# Clean up previous build collateral.
rm -rf .coverage *.egg-info dist docs/build docs/source/*.rst conda-recipe/build .pytest_cache \
       anaconda/opentelemetry/__pycache__ tests/__pycache__ docs/source/__pycache__ htmlcov \
       version.txt
