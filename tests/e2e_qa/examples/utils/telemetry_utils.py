# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Telemetry Utilities for E2E QA Examples

This module provides utilities for managing telemetry operations including
flushing telemetry data to backends.

Usage:
    # Flush all providers at once (convenience)
    flush_telemetry()
    
    # Flush only specific providers (atomic operations)
    flush_metrics()
    flush_traces()
    flush_logs()
    
    # Flush with custom timeout
    flush_metrics(timeout_millis=10000)
"""

from opentelemetry import metrics, trace
from anaconda.opentelemetry.signals import _AnacondaLogger
from .print_utils import print_flush_status


def flush_metrics(timeout_millis: int = 5000):
    """
    Flush metrics provider.
    
    Args:
        timeout_millis: Timeout in milliseconds (default: 5000)
    """
    meter_provider = metrics.get_meter_provider()
    if hasattr(meter_provider, 'force_flush'):
        meter_provider.force_flush(timeout_millis=timeout_millis)


def flush_traces(timeout_millis: int = 5000):
    """
    Flush traces provider.
    
    Args:
        timeout_millis: Timeout in milliseconds (default: 5000)
    """
    tracer_provider = trace.get_tracer_provider()
    if hasattr(tracer_provider, 'force_flush'):
        tracer_provider.force_flush(timeout_millis=timeout_millis)


def flush_logs(timeout_millis: int = 5000):
    """
    Flush logs provider.
    
    Args:
        timeout_millis: Timeout in milliseconds (default: 5000)
    """
    if _AnacondaLogger._instance:
        logger_instance = _AnacondaLogger._instance
        if hasattr(logger_instance, '_provider') and logger_instance._provider:
            logger_instance._provider.force_flush(timeout_millis=timeout_millis)


def flush_telemetry():
    """
    Flush all telemetry providers (metrics, traces, logs).
    
    This is a convenience function that calls flush_metrics(), flush_traces(),
    and flush_logs() in sequence. Use the individual functions if you only
    need to flush specific providers.
    """
    flush_metrics()
    flush_traces()
    flush_logs()
    print_flush_status(success=True)
