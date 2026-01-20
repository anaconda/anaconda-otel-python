# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Metric-related test data constants

Contains metric names, values, and attributes used for testing
telemetry functionality.
"""

from enum import Enum


class MetricName(str, Enum):
    """Metric names for each example"""
    EXAMPLE_01 = 'example_01_initialization_test'
    EXAMPLE_02 = 'example_02_metrics_test'
    EXAMPLE_03 = 'example_03_default_test'
    EXAMPLE_04 = 'example_04_selective_test'
    EXAMPLE_05 = 'example_05_complete_test'
    EXAMPLE_06 = 'example_06_env_based_test'
    EXAMPLE_07 = 'example_07_flush_test'


class MetricValue(int, Enum):
    """Metric values"""
    INCREMENT_BY_ONE = 1
    INCREMENT_BY_FIVE = 5
    INCREMENT_BY_TEN = 10
