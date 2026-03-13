import threading, logging
from enum import Enum
from typing import Optional
from opentelemetry.sdk.metrics.export import MetricExporter
from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.sdk._logs.export import LogExporter

from anaconda_opentelemetry.oidc import OIDCAuthenticator


class ExporterState(Enum):
    READY = 1
    UPDATING = 2


class _OTLPExporterMixin:
    """Mixin that provides common functionality for all OTLP exporter shims"""

    def __init__(self, exporter_class, oidc_authenticator: Optional[OIDCAuthenticator] = None, **kwargs):
        self._logger = logging.getLogger('exporter_shim_logger')
        self._lock = threading.Lock()
        self._exporter_class = exporter_class
        self._oidc_authenticator = oidc_authenticator
        self._init_kwargs = kwargs
        self._headers = kwargs.get('headers')
        self._last_token: Optional[str] = self._headers.get('authorization') if self._headers else None
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
    
    def _refresh_headers_if_needed(self):
        if self._oidc_authenticator is None or self._headers is None:
            return
        token = self._oidc_authenticator.get_token()
        bearer = f"Bearer {token}"
        if bearer != self._last_token:
            self._headers['authorization'] = bearer
            self._last_token = bearer

    def export(self, *args, **kwargs):
        try:
            self._refresh_headers_if_needed()
            return self._exporter.export(*args, **kwargs)
        except Exception as exception:
            self._logger.error(f"Failed to export: {exception}")
            return False
            
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