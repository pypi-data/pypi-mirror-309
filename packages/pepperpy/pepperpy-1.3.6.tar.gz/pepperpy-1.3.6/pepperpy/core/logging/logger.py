"""Logging utilities"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Protocol

from .exceptions import LoggingError
from .formatters import JsonFormatter
from .handlers import AsyncHandler


@dataclass
class LogRecord:
    """Log record data"""

    level: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


class LogHandler(Protocol):
    """Log handler protocol"""

    async def handle(self, record: dict[str, Any]) -> None: ...


class Logger:
    """Async logger implementation"""

    def __init__(self, name: str):
        self.name = name
        self._handlers: list[LogHandler] = []
        self._formatter = JsonFormatter()

    def add_handler(self, handler: LogHandler) -> None:
        """Add log handler"""
        self._handlers.append(handler)

    async def log(self, level: str, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log message with metadata"""
        try:
            record = LogRecord(level=level, message=msg, metadata=kwargs)
            record_dict = {
                "level": record.level,
                "message": record.message,
                "timestamp": record.timestamp.isoformat(),
                **record.metadata,
            }
            await asyncio.gather(*(handler.handle(record_dict) for handler in self._handlers))
        except Exception as e:
            raise LoggingError(f"Failed to log message: {e!s}", cause=e)

    async def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log debug message"""
        await self.log("DEBUG", msg, *args, **kwargs)

    async def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log info message"""
        await self.log("INFO", msg, *args, **kwargs)

    async def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log warning message"""
        await self.log("WARNING", msg, *args, **kwargs)

    async def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log error message"""
        await self.log("ERROR", msg, *args, **kwargs)

    async def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log critical message"""
        await self.log("CRITICAL", msg, *args, **kwargs)


_loggers: dict[str, Logger] = {}


def get_logger(name: str) -> Logger:
    """Get or create logger by name"""
    if name not in _loggers:
        logger = Logger(name)
        logger.add_handler(AsyncHandler())
        _loggers[name] = logger
    return _loggers[name]
