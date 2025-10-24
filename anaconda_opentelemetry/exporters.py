import threading
# from .config import Configuration
from opentelemetry.sdk.metrics.export import MetricExporter

class OTLPExporterShim(MetricExporter):
    
    @staticmethod
    def _derive_signal(exporter_class):
        class_name = exporter_class.__name__.lower()
        if 'metric' in class_name:
            return 'metrics'
        elif 'span' in class_name or 'trace' in class_name:
            return 'tracing'
        elif 'log' in class_name:
            return 'logging'
        else:
            raise ValueError(f"Cannot determine signal type for {exporter_class.__name__}")
        
    def __init__(self, exporter_class, **kwargs):
        self._lock = threading.Lock()
        self._exporter_class = exporter_class
        self._init_kwargs = kwargs
        self._exporter = exporter_class(**kwargs)
        self._signal = self._derive_signal(exporter_class)
    
    def update_endpoint(self, config, new_endpoint, auth_token=None):
        with self._lock:
            # Update config
            set_endpoint = getattr(config, f"set_{self._signal}_endpoint", None)
            set_endpoint(new_endpoint, auth_token=auth_token)
            get_endpoint = getattr(config, f"_get_{self._signal}_endpoint", None)
            endpoint = get_endpoint()
            self._exporter.force_flush()
            self._exporter.shutdown()
            self._init_kwargs['endpoint'] = endpoint
            self._exporter = self._exporter_class(**self._init_kwargs)
        return True
    
    def export(self, *args, **kwargs):
        return self._exporter.export(*args, **kwargs)
    
    def force_flush(self, *args, **kwargs):
        return self._exporter.force_flush(*args, **kwargs)
    
    def shutdown(self, *args, **kwargs):
        return self._exporter.shutdown(*args, **kwargs)
    
    @property
    def _preferred_temporality(self):
        return self._exporter._preferred_temporality
    
    @property
    def _preferred_aggregation(self):
        return self._exporter._preferred_aggregation