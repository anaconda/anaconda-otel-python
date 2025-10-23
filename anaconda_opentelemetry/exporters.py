from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter as OTLPMetricExporterHTTP
import threading
from .config import Configuration

class DynamicOTLPExporterHTTP(OTLPMetricExporterHTTP):
    def __init__(self, **kwargs):
        self._lock = threading.Lock()
        self._init_kwargs = kwargs
        super().__init__(**kwargs)
    
    def update_endpoint(
            self,
            config: Configuration,
            signal: str,
            new_endpoint: str,
            auth_token: str = None
    ) -> bool:
        set_endpoint_method = getattr(config, f"set_{signal}_endpoint", None)
        if callable(set_endpoint_method):
            set_endpoint_method(new_endpoint, auth_token=auth_token)
        else:
            return False
        get_endpoint_method = getattr(config, f"_get_{signal}_endpoint", None)
        if not callable(get_endpoint_method):
            return False
        endpoint = get_endpoint_method()

        with self._lock:
            self.force_flush()
            self.shutdown()
            self._init_kwargs['endpoint'] = endpoint
            super().__init__(**self._init_kwargs)

        return True