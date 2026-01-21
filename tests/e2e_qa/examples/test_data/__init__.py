# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Test Data Constants for E2E Examples

This module provides centralized test data constants used across all examples.
Organizing test data in one place makes it easier to maintain consistency
and update values when needed. All constants are defined as Enums for type safety.
"""

from .service_data import (
    ServiceName,
    ServiceVersion,
    Environment,
    Platform
)

from .metric_data import (
    MetricName,
    MetricValue
)

from .attribute_data import (
    CustomAttributes,
    DeploymentAttributes,
    UserId,
    Hostname,
    TestType,
    AutoDetectedAttributes
)

from .config_data import (
    ExportInterval,
    LoggingLevel,
    SignalTypes
)

from .logging_data import (
    LogLevel,
    LogMessage,
    LogAttributes,
    LoggerName,
    ServiceNameLogging
)

from .metrics_examples_data import (
    ServiceNameMetrics,
    CounterName,
    UpDownCounterName,
    HistogramName,
    MetricAttributes,
    MetricValues,
    MetricDescriptions
)

__all__ = [
    # Service data
    'ServiceName',
    'ServiceVersion',
    'Environment',
    'Platform',
    
    # Metric data
    'MetricName',
    'MetricValue',
    
    # Attribute data
    'CustomAttributes',
    'DeploymentAttributes',
    'UserId',
    'Hostname',
    'TestType',
    'AutoDetectedAttributes',
    
    # Config data
    'ExportInterval',
    'LoggingLevel',
    'SignalTypes',
    
    # Logging data
    'LogLevel',
    'LogMessage',
    'LogAttributes',
    'LoggerName',
    'ServiceNameLogging',
    
    # Metrics examples data
    'ServiceNameMetrics',
    'CounterName',
    'UpDownCounterName',
    'HistogramName',
    'MetricAttributes',
    'MetricValues',
    'MetricDescriptions',
]
