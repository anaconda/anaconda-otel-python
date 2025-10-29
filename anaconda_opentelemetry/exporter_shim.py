import threading
from enum import Enum
from opentelemetry.sdk.metrics.export import MetricExporter
from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.sdk._logs.export import LogExporter


class ExporterState(Enum):
    READY = 1
    UPDATING = 2


class _OTLPExporterMixin:
    """Mixin that provides common functionality for all OTLP exporter shims"""
    
    def __init__(self, exporter_class, **kwargs):
        self._lock = threading.Lock()
        self._exporter_class = exporter_class
        self._init_kwargs = kwargs
        self._exporter = exporter_class(**kwargs)
        self._state = ExporterState.READY
    
    def change_signal_endpoint(self, batch_access, config, new_endpoint, auth_token=None):

        endpoint = config._change_signal_endpoint(
            self._signal,
            new_endpoint,
            auth_token=auth_token
        )
        self._init_kwargs['endpoint'] = endpoint

        with self._lock:
            self._state = ExporterState.UPDATING

        try:
            new_exporter = self._exporter_class(**self._init_kwargs)
        except:
            with self._lock:
                self._state = ExporterState.READY
            return
        
        with self._lock:
            old_exporter = self._exporter
            batch_access.force_flush()
            old_exporter.shutdown()
            self._exporter = new_exporter
            self._state = ExporterState.READY

        return True
    
    def export(self, *args, **kwargs):
        return self._exporter.export(*args, **kwargs)
    
    def shutdown(self, *args, **kwargs):
        return self._exporter.shutdown(*args, **kwargs)
    
    def force_flush(self, *args, **kwargs):
        # this function doesn't need tests, it must be implemented but exporter method is stub
        return self._exporter.force_flush(*args, **kwargs)
    

class OTLPMetricExporterShim(_OTLPExporterMixin, MetricExporter):
    _signal = 'metrics'

    @property
    def _preferred_temporality(self):
        return self._exporter._preferred_temporality
    
    @property
    def _preferred_aggregation(self):
        return self._exporter._preferred_aggregation


class OTLPSpanExporterShim(_OTLPExporterMixin, SpanExporter):
    _signal = 'tracing'


class OTLPLogExporterShim(_OTLPExporterMixin, LogExporter):
    _signal = 'logging'