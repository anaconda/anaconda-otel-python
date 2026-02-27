import warnings
from opentelemetry.sdk._logs import LogDeprecatedInitWarning
warnings.filterwarnings(
    "ignore",
    category=LogDeprecatedInitWarning,
    message=".*LogRecord will be removed.*",
)

from opentelemetry.sdk._logs import LoggerProvider, LogRecord
from opentelemetry._logs.severity import SeverityNumber
from .custom_types import AttrDict

class SilentLogger:
    """
    Emits log records purely as OTel log telemetry, bypassing Python's
    logging hierarchy so they never appear in console/file handlers or
    interfere with developer log levels. Optional way to export logs,
    the Python logging module is supported as well.
    """

    def __init__(
        self,
        provider: LoggerProvider,
        logger_name: str = "silent_logger",
        default_severity: SeverityNumber = SeverityNumber.INFO,
    ):
        self._logger = provider.get_logger(logger_name)
        self._default_severity = default_severity

    def emit(
        self,
        body: str,
        severity: SeverityNumber | None = None,
        attributes: AttrDict={},
    ):
        record = LogRecord(
            body=body,
            severity_number=severity or self._default_severity,
            attributes=attributes,
        )
        self._logger.emit(record)

    def INFO(self, body: str, attributes: AttrDict={}):
        self.emit(body, SeverityNumber.INFO, attributes)

    def WARN(self, body: str, attributes: AttrDict={}):
        self.emit(body, SeverityNumber.WARN, attributes)

    def ERROR(self, body: str, attributes: AttrDict={}):
        self.emit(body, SeverityNumber.ERROR, attributes)

    def DEBUG(self, body: str, attributes: AttrDict={}):
        self.emit(body, SeverityNumber.DEBUG, attributes)