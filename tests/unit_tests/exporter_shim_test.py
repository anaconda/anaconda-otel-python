# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

import sys
sys.path.append("./")

import pytest
import threading
from unittest.mock import Mock, MagicMock, patch, call
from enum import Enum

from anaconda_opentelemetry.exporter_shim import (
    ExporterState,
    _OTLPExporterMixin,
    OTLPMetricExporterShim,
    OTLPSpanExporterShim,
    OTLPLogExporterShim
)


class MockExporter:
    """Mock exporter class for testing"""
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.exported_items = []
        self.is_shutdown = False
        self.is_flushed = False
        
    def export(self, items):
        self.exported_items.append(items)
        return "SUCCESS"
    
    def shutdown(self):
        self.is_shutdown = True
        return True
    
    def force_flush(self, timeout=None):
        self.is_flushed = True
        return True


class MockMetricExporter(MockExporter):
    """Mock metric exporter with temporality and aggregation properties"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._preferred_temporality = "CUMULATIVE"
        self._preferred_aggregation = "SUM"


class TestExporterState:
    def test_exporter_state_enum_values(self):
        assert ExporterState.READY.value == 1
        assert ExporterState.UPDATING.value == 2
        
    def test_exporter_state_enum_members(self):
        assert hasattr(ExporterState, 'READY')
        assert hasattr(ExporterState, 'UPDATING')
        assert len(ExporterState) == 2


class TestOTLPExporterMixin:
    def test_initialization(self):
        mixin = _OTLPExporterMixin(MockExporter, endpoint="http://localhost:4317")
        
        assert mixin._exporter_class == MockExporter
        assert mixin._init_kwargs == {"endpoint": "http://localhost:4317"}
        assert isinstance(mixin._exporter, MockExporter)
        assert mixin._state == ExporterState.READY
        assert isinstance(mixin._lock, threading.Lock)
        
    def test_initialization_with_multiple_kwargs(self):
        kwargs = {
            "endpoint": "http://localhost:4317",
            "headers": {"Authorization": "Bearer token"},
            "timeout": 30
        }
        mixin = _OTLPExporterMixin(MockExporter, **kwargs)
        
        assert mixin._init_kwargs == kwargs
        assert mixin._exporter.kwargs == kwargs
        
    def test_export_delegates_to_exporter(self):
        mixin = _OTLPExporterMixin(MockExporter)
        items = ["item1", "item2"]
        
        result = mixin.export(items)
        
        assert result == "SUCCESS"
        assert mixin._exporter.exported_items == [items]
        
    def test_shutdown_delegates_to_exporter(self):
        mixin = _OTLPExporterMixin(MockExporter)
        
        result = mixin.shutdown()
        
        assert result == True
        assert mixin._exporter.is_shutdown == True
        
    def test_force_flush_delegates_to_exporter(self):
        mixin = _OTLPExporterMixin(MockExporter)
        
        result = mixin.force_flush(timeout=10)
        
        assert result == True
        assert mixin._exporter.is_flushed == True
        
    def test_update_endpoint_successful(self):
        mixin = _OTLPExporterMixin(MockExporter, endpoint="http://localhost:4317")
        mixin._signal = "metrics"
        
        config = Mock()
        config._change_signal_endpoint.return_value = "http://newhost:8080/v1/metrics"
        
        batch_access = Mock()
        
        result = mixin.update_endpoint(
            batch_access,
            config,
            "http://newhost:8080",
            auth_token="token123"
        )
        
        assert result == True
        assert mixin._init_kwargs['endpoint'] == "http://newhost:8080/v1/metrics"
        assert mixin._state == ExporterState.READY
        
        config._change_signal_endpoint.assert_called_once_with(
            "metrics",
            "http://newhost:8080",
            auth_token="token123"
        )
        
        batch_access.force_flush.assert_called_once()
        
        assert isinstance(mixin._exporter, MockExporter)
        assert mixin._exporter.kwargs['endpoint'] == "http://newhost:8080/v1/metrics"
        
    def test_update_endpoint_without_auth_token(self):
        mixin = _OTLPExporterMixin(MockExporter, endpoint="http://localhost:4317")
        mixin._signal = "tracing"
        
        config = Mock()
        config._change_signal_endpoint.return_value = "http://newhost:8080/v1/traces"
        
        batch_access = Mock()
        
        result = mixin.update_endpoint(
            batch_access,
            config,
            "http://newhost:8080"
        )
        
        assert result == True
        config._change_signal_endpoint.assert_called_once_with(
            "tracing",
            "http://newhost:8080",
            auth_token=None
        )
        
    def test_update_endpoint_handles_exporter_creation_failure(self):
        class FailingExporter:
            def __init__(self, **kwargs):
                if kwargs.get('endpoint') == "http://invalid:8080/v1/metrics":
                    raise ValueError("Invalid endpoint")
                self.kwargs = kwargs
                self.is_shutdown = False
                
            def shutdown(self):
                self.is_shutdown = True
                
        mixin = _OTLPExporterMixin(FailingExporter, endpoint="http://localhost:4317")
        mixin._signal = "metrics"
        old_exporter = mixin._exporter
        
        config = Mock()
        config._change_signal_endpoint.return_value = "http://invalid:8080/v1/metrics"
        
        batch_access = Mock()
        
        result = mixin.update_endpoint(
            batch_access,
            config,
            "http://invalid:8080"
        )
        
        assert result is None
        assert mixin._state == ExporterState.READY
        assert mixin._exporter is old_exporter
        batch_access.force_flush.assert_not_called()
        
    def test_update_endpoint_state_transitions(self):
        mixin = _OTLPExporterMixin(MockExporter, endpoint="http://localhost:4317")
        mixin._signal = "logging"
        
        config = Mock()
        config._change_signal_endpoint.return_value = "http://newhost:8080/v1/logs"
        
        batch_access = Mock()
        
        states_observed = []
        original_lock = mixin._lock
        mock_lock = MagicMock()
        
        def track_state_on_enter(*args):
            states_observed.append(mixin._state)
            return original_lock.__enter__()
        
        def track_state_on_exit(*args):
            states_observed.append(mixin._state)
            return original_lock.__exit__(*args)
            
        mock_lock.__enter__ = Mock(side_effect=track_state_on_enter)
        mock_lock.__exit__ = Mock(side_effect=track_state_on_exit)
        mock_lock.acquire = original_lock.acquire
        mock_lock.release = original_lock.release
        
        mixin._lock = mock_lock
        
        mixin.update_endpoint(batch_access, config, "http://newhost:8080")
        
        assert ExporterState.UPDATING in states_observed
        assert mixin._state == ExporterState.READY
        
    def test_update_endpoint_thread_safety(self):
        """Test that update_endpoint properly locks during state changes"""
        mixin = _OTLPExporterMixin(MockExporter, endpoint="http://localhost:4317")
        mixin._signal = "metrics"
        
        config = Mock()
        config._change_signal_endpoint.return_value = "http://newhost:8080/v1/metrics"
        
        batch_access = Mock()
        
        original_lock = mixin._lock
        mock_lock = MagicMock()
        
        enter_count = [0]
        def count_enter(*args):
            enter_count[0] += 1
            return original_lock.__enter__()
            
        mock_lock.__enter__ = Mock(side_effect=count_enter)
        mock_lock.__exit__ = Mock(side_effect=lambda *args: original_lock.__exit__(*args))
        mock_lock.acquire = original_lock.acquire
        mock_lock.release = original_lock.release
        
        mixin._lock = mock_lock
        
        mixin.update_endpoint(batch_access, config, "http://newhost:8080")
        
        # Should acquire lock at least twice
        assert enter_count[0] >= 2
        assert mock_lock.__enter__.call_count == mock_lock.__exit__.call_count


class TestOTLPMetricExporterShim:
    def test_signal_property(self):
        assert OTLPMetricExporterShim._signal == 'metrics'
        
    def test_initialization(self):
        shim = OTLPMetricExporterShim(MockMetricExporter, endpoint="http://localhost:4317")
        
        assert isinstance(shim._exporter, MockMetricExporter)
        assert shim._signal == 'metrics'
        
    def test_properties_follow_exporter_changes(self):
        shim = OTLPMetricExporterShim(MockMetricExporter)
        
        shim._exporter._preferred_temporality = "DELTA"
        shim._exporter._preferred_aggregation = "HISTOGRAM"
        
        assert shim._preferred_temporality == "DELTA"
        assert shim._preferred_aggregation == "HISTOGRAM"
        
    def test_composition_of_metric_exporter(self):
        from opentelemetry.sdk.metrics.export import MetricExporter
        
        shim = OTLPMetricExporterShim(MockMetricExporter)
        assert isinstance(shim, MetricExporter)
        
    def test_export_with_metrics(self):
        shim = OTLPMetricExporterShim(MockMetricExporter)
        
        metrics = [{"name": "cpu_usage", "value": 75.5}]
        result = shim.export(metrics)
        
        assert result == "SUCCESS"
        assert shim._exporter.exported_items == [metrics]


class TestOTLPSpanExporterShim:
    def test_signal_property(self):
        assert OTLPSpanExporterShim._signal == 'tracing'
        
    def test_initialization(self):
        shim = OTLPSpanExporterShim(MockExporter, endpoint="http://localhost:4317")
        
        assert isinstance(shim._exporter, MockExporter)
        assert shim._signal == 'tracing'
        
    def test_inherits_from_span_exporter(self):
        from opentelemetry.sdk.trace.export import SpanExporter
        
        shim = OTLPSpanExporterShim(MockExporter)
        assert isinstance(shim, SpanExporter)
        
    def test_export_with_spans(self):
        shim = OTLPSpanExporterShim(MockExporter)
        
        spans = [{"trace_id": "123", "span_id": "456"}]
        result = shim.export(spans)
        
        assert result == "SUCCESS"
        assert shim._exporter.exported_items == [spans]
        
    def test_update_endpoint_uses_tracing_signal(self):
        shim = OTLPSpanExporterShim(MockExporter)
        
        config = Mock()
        config._change_signal_endpoint.return_value = "http://newhost:8080/v1/traces"
        
        batch_access = Mock()
        
        shim.update_endpoint(batch_access, config, "http://newhost:8080")
        
        config._change_signal_endpoint.assert_called_once_with(
            "tracing",
            "http://newhost:8080",
            auth_token=None
        )


class TestOTLPLogExporterShim:
    def test_signal_property(self):
        assert OTLPLogExporterShim._signal == 'logging'
        
    def test_initialization(self):
        shim = OTLPLogExporterShim(MockExporter, endpoint="http://localhost:4317")
        
        assert isinstance(shim._exporter, MockExporter)
        assert shim._signal == 'logging'
        
    def test_inherits_from_log_exporter(self):
        from opentelemetry.sdk._logs.export import LogExporter
        
        shim = OTLPLogExporterShim(MockExporter)
        assert isinstance(shim, LogExporter)
        
    def test_export_with_logs(self):
        shim = OTLPLogExporterShim(MockExporter)
        
        logs = [{"level": "INFO", "message": "Test log"}]
        result = shim.export(logs)
        
        assert result == "SUCCESS"
        assert shim._exporter.exported_items == [logs]
        
    def test_update_endpoint_uses_logging_signal(self):
        shim = OTLPLogExporterShim(MockExporter)
        
        config = Mock()
        config._change_signal_endpoint.return_value = "http://newhost:8080/v1/logs"
        
        batch_access = Mock()
        
        shim.update_endpoint(batch_access, config, "http://newhost:8080")
        
        config._change_signal_endpoint.assert_called_once_with(
            "logging",
            "http://newhost:8080",
            auth_token=None
        )