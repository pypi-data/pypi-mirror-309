"""Event system for inter-module communication"""

import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum
from typing import Any


class Priority(IntEnum):
    """Event handler priority"""

    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class Handler:
    """Event handler with priority"""

    callback: Callable
    priority: Priority


class EventBus:
    """Event bus for pub/sub communication"""

    def __init__(self):
        self._handlers: dict[str, list[Handler]] = {}

    async def publish(
        self, event: str, data: Any = None, priority: Priority | None = None,
    ) -> None:
        """Publish event"""
        if event in self._handlers:
            handlers = self._handlers[event]

            # Filter by priority if specified
            if priority is not None:
                handlers = [h for h in handlers if h.priority >= priority]

            # Sort by priority (high to low)
            handlers.sort(key=lambda h: h.priority, reverse=True)

            # Execute handlers
            tasks = [handler.callback(data) for handler in handlers]
            await asyncio.gather(*tasks)

    def subscribe(
        self, event: str, handler: Callable, priority: Priority = Priority.NORMAL,
    ) -> None:
        """Subscribe to event with priority"""
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append(Handler(handler, priority))

    def unsubscribe(self, event: str, handler: Callable) -> None:
        """Unsubscribe from event"""
        if event in self._handlers:
            self._handlers[event] = [h for h in self._handlers[event] if h.callback != handler]


events = EventBus()
