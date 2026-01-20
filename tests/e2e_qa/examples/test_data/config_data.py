# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Configuration test data constants

Contains export intervals, logging levels, timeout values, and other
configuration-related constants used in examples.
"""

from enum import Enum


class ExportInterval(int, Enum):
    """Export intervals (in milliseconds)"""
    METRICS_15S = 15000
    METRICS_30S = 30000
    METRICS_60S = 60000
    TRACING_15S = 15000
    TRACING_30S = 30000


class LoggingLevel(str, Enum):
    """Logging levels"""
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'


class SignalTypes(Enum):
    """Signal type combinations for telemetry initialization"""
    ALL_SIGNALS = ['metrics', 'logging', 'tracing']
    METRICS_ONLY = ['metrics']
    METRICS_AND_TRACING = ['metrics', 'tracing']
    LOGGING_ONLY = ['logging']
    TRACING_ONLY = ['tracing']
