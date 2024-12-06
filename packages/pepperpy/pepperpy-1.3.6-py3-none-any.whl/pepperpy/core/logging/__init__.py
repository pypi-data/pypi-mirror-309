"""Core logging module"""

import logging
import sys
from typing import Any, Protocol

from .config import LogConfig, LogLevel
from .logger import Logger


class SyncLogger(Protocol):
    """Protocol for synchronous logging"""

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None: ...


class AsyncLogger(Protocol):
    """Protocol for asynchronous logging"""

    async def debug(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    async def info(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    async def warning(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    async def error(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    async def critical(self, msg: str, *args: Any, **kwargs: Any) -> None: ...


class LoggerAdapter:
    """Adapter for Python's standard logging with sync/async support"""

    def __init__(self, logger: logging.Logger):
        self._logger = logger
        self._sync_logger = self._create_sync_logger()
        self._async_logger = self._create_async_logger()

    def _create_sync_logger(self) -> SyncLogger:
        """Create synchronous logger interface"""
        return self._logger

    def _create_async_logger(self) -> AsyncLogger:
        """Create asynchronous logger interface"""
        return Logger(self._logger.name)

    @property
    def sync(self) -> SyncLogger:
        """Get synchronous logger interface"""
        return self._sync_logger

    @property
    def async_(self) -> AsyncLogger:
        """Get asynchronous logger interface"""
        return self._async_logger

    # Implementação dos métodos de logging diretos
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log debug message synchronously"""
        self.sync.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log info message synchronously"""
        self.sync.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log warning message synchronously"""
        self.sync.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log error message synchronously"""
        self.sync.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log critical message synchronously"""
        self.sync.critical(msg, *args, **kwargs)

    async def async_debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log debug message asynchronously"""
        await self.async_.debug(msg, *args, **kwargs)

    async def async_info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log info message asynchronously"""
        await self.async_.info(msg, *args, **kwargs)

    async def async_warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log warning message asynchronously"""
        await self.async_.warning(msg, *args, **kwargs)

    async def async_error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log error message asynchronously"""
        await self.async_.error(msg, *args, **kwargs)

    async def async_critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log critical message asynchronously"""
        await self.async_.critical(msg, *args, **kwargs)


def get_logger(name: str, config: LogConfig | None = None) -> LoggerAdapter:
    """Get configured logger instance"""
    logger = logging.getLogger(name)

    if config is None:
        config = LogConfig(name=name, version="0.1.0", level=LogLevel.INFO)

    logger.setLevel(config.level.value)

    if config.console_enabled:
        from rich.logging import RichHandler

        console_handler = RichHandler(
            rich_tracebacks=True,
            show_time=True,
            show_path=True,
            enable_link_path=True,
            markup=config.colors_enabled,
        )
        console_handler.setLevel(config.level.value)
        logger.addHandler(console_handler)

    if config.file_path:
        file_handler = logging.FileHandler(config.file_path)
        file_handler.setLevel(config.level.value)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
        )
        logger.addHandler(file_handler)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(handler)

    return LoggerAdapter(logger)


__all__ = ["LogLevel", "LogConfig", "get_logger", "Logger"]
