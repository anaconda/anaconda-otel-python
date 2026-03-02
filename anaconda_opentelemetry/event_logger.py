import warnings
from opentelemetry.sdk._logs import LogDeprecatedInitWarning
warnings.filterwarnings(
    "ignore",
    category=LogDeprecatedInitWarning,
    message=".*LogRecord will be removed.*",
)

from opentelemetry.sdk._logs import LoggerProvider, LogRecord
from .formatting import AttrDict, log_event_name_key


class EventLogger:
    """
    Emits log records purely as OTel log telemetry, bypassing Python's
    logging hierarchy so they never appear in console/file handlers or
    interfere with developer log levels. Optional way to export logs,
    the Python logging module is supported as well.
    """

    def __init__(
        self,
        provider: LoggerProvider,
        logger_name: str = "event_logger",
    ):
        self._logger = provider.get_logger(logger_name)

    def _send_event(
        self,
        body: str,
        event_name: str,
        attributes: AttrDict={},
    ):
        # update attributes with event name - mandatory for event logs
        attributes.update({log_event_name_key: event_name})
        record = LogRecord(
            body=body,
            attributes=attributes,
        )
        self._logger.emit(record)