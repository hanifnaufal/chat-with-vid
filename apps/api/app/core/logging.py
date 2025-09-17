import logging
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as a JSON string."""
        log_entry = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in [
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "process",
                "exc_info",
                "exc_text",
                "stack_info",
            ]:
                log_entry[key] = value

        return json.dumps(log_entry)


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Set up and configure the application logger.

    Args:
        level: The logging level to use (default: INFO).

    Returns:
        The configured logger instance.
    """
    # Create logger
    logger = logging.getLogger("chat_with_vid_api")
    logger.setLevel(level)

    # Prevent adding multiple handlers if setup_logging is called multiple times
    if not logger.handlers:
        # Create handler
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())

        # Add handler to logger
        logger.addHandler(handler)

    return logger
