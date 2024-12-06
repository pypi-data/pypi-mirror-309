"""Metrics collection implementation"""

import asyncio
from typing import Any

from pepperpy.core.module import BaseModule, ModuleMetadata

from .config import MetricsConfig
from .exceptions import MetricsError
from .types import MetricEvent, MetricType


class MetricsCollector(BaseModule):
    """Collector for AI operation metrics"""

    def __init__(self, config: MetricsConfig | None = None):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="metrics",
            version="1.0.0",
            description="AI metrics collection",
            dependencies=[],
            config=config.dict() if config else {},
        )
        self._events: list[MetricEvent] = []
        self._flush_task = None

    async def _setup(self) -> None:
        """Initialize metrics collector"""
        if self.config.get("auto_flush_enabled", True):
            self._flush_task = asyncio.create_task(self._auto_flush())

    async def _cleanup(self) -> None:
        """Cleanup metrics collector"""
        if self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass
        await self.flush()

    async def record(
        self,
        type: MetricType,
        value: Any,
        module: str,
        operation: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Record a metric event"""
        event = MetricEvent(
            type=type, value=value, module=module, operation=operation, metadata=metadata or {},
        )
        self._events.append(event)

        # Check if we should flush
        if len(self._events) >= self.config.get("flush_threshold", 100):
            await self.flush()

    async def flush(self) -> None:
        """Flush collected metrics"""
        if not self._events:
            return

        try:
            # Get storage backend
            backend = self.config.get("storage_backend", "memory")

            if backend == "memory":
                # Just keep in memory
                pass
            elif backend == "file":
                await self._flush_to_file()
            elif backend == "custom":
                await self._flush_to_custom()

            # Clear events after successful flush
            self._events.clear()

        except Exception as e:
            raise MetricsError("Failed to flush metrics", cause=e)

    async def _auto_flush(self) -> None:
        """Automatically flush metrics periodically"""
        interval = self.config.get("flush_interval", 60)  # seconds
        while True:
            await asyncio.sleep(interval)
            await self.flush()

    async def _flush_to_file(self) -> None:
        """Flush metrics to file"""
        if not self.config.get("file_path"):
            raise MetricsError("File path not configured for metrics storage")

        try:
            import json
            from pathlib import Path

            path = Path(self.config["file_path"])
            path.parent.mkdir(parents=True, exist_ok=True)

            # Convert events to serializable format
            events = [
                {
                    "type": e.type.value,
                    "value": e.value,
                    "module": e.module,
                    "operation": e.operation,
                    "timestamp": e.timestamp.isoformat(),
                    "metadata": e.metadata,
                }
                for e in self._events
            ]

            # Append to file
            with path.open("a") as f:
                for event in events:
                    f.write(json.dumps(event) + "\n")

        except Exception as e:
            raise MetricsError(f"Failed to write metrics to file: {e!s}", cause=e)

    async def _flush_to_custom(self) -> None:
        """Flush metrics to custom handler"""
        handler = self.config.get("custom_handler")
        if not handler or not callable(handler):
            raise MetricsError("Custom handler not configured for metrics storage")

        try:
            result = handler(self._events)
            if asyncio.iscoroutine(result):
                await result
        except Exception as e:
            raise MetricsError(f"Custom handler failed: {e!s}", cause=e)
