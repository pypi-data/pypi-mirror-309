"""Execution tracing utilities"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from pepperpy.core.exceptions import PepperPyError


class TracingError(PepperPyError):
    """Tracing error"""


@dataclass
class TraceEvent:
    """Trace event information"""

    name: str
    category: str
    timestamp: datetime = field(default_factory=datetime.now)
    duration: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class Tracer:
    """Execution tracer"""

    def __init__(self):
        self._events: list[TraceEvent] = []
        self._active_spans: dict[str, TraceEvent] = {}

    def start_span(
        self, name: str, category: str, metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Start a new trace span

        Args:
            name: Span name
            category: Span category
            metadata: Additional span metadata

        """
        if name in self._active_spans:
            raise TracingError(f"Span already active: {name}")

        event = TraceEvent(
            name=name,
            category=category,
            metadata=metadata or {},
        )
        self._active_spans[name] = event

    def end_span(self, name: str, metadata: dict[str, Any] | None = None) -> None:
        """
        End an active trace span

        Args:
            name: Span name
            metadata: Additional span metadata

        """
        if name not in self._active_spans:
            raise TracingError(f"Span not active: {name}")

        event = self._active_spans[name]
        event.duration = (datetime.now() - event.timestamp).total_seconds()
        if metadata:
            event.metadata.update(metadata)

        self._events.append(event)
        del self._active_spans[name]

    def add_event(
        self,
        name: str,
        category: str,
        duration: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Add a trace event

        Args:
            name: Event name
            category: Event category
            duration: Event duration in seconds
            metadata: Additional event metadata

        """
        event = TraceEvent(
            name=name,
            category=category,
            duration=duration,
            metadata=metadata or {},
        )
        self._events.append(event)

    def get_events(self, category: str | None = None) -> list[TraceEvent]:
        """
        Get recorded trace events

        Args:
            category: Filter events by category

        Returns:
            List[TraceEvent]: List of trace events

        """
        if category is None:
            return self._events.copy()
        return [event for event in self._events if event.category == category]

    def clear(self) -> None:
        """Clear all recorded events"""
        self._events.clear()
        self._active_spans.clear()


# Global tracer instance
tracer = Tracer()
