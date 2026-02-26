from opentelemetry.sdk._logs import LoggerProvider, LogRecord
# from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs.severity import SeverityNumber


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
        attributes: dict | None = None,
    ):
        """Emit a log record directly to the OTel pipeline."""
        record = LogRecord(
            body=body,
            severity_number=severity or self._default_severity,
            attributes=attributes,
        )
        self._logger.emit(record)