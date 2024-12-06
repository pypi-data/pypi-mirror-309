"""State management utilities"""

from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from pepperpy.core.exceptions import PepperPyError


class StateError(PepperPyError):
    """State management error"""


T = TypeVar("T")


@dataclass
class State(Generic[T]):
    """Application state container"""

    data: T
    metadata: dict[str, Any] = field(default_factory=dict)
    version: int = 1


class StateManager:
    """State manager for handling application state"""

    def __init__(self):
        self._states: dict[str, State[Any]] = {}

    def set_state(self, name: str, data: Any, metadata: dict[str, Any] | None = None) -> None:
        """
        Set state value

        Args:
            name: State name
            data: State data
            metadata: Optional state metadata

        """
        if name in self._states:
            current = self._states[name]
            version = current.version + 1
        else:
            version = 1

        self._states[name] = State(
            data=data,
            metadata=metadata or {},
            version=version,
        )

    def get_state(self, name: str) -> State[Any] | None:
        """
        Get state value

        Args:
            name: State name

        Returns:
            Optional[State[Any]]: State value if exists

        """
        return self._states.get(name)

    def remove_state(self, name: str) -> None:
        """
        Remove state value

        Args:
            name: State name

        """
        if name in self._states:
            del self._states[name]

    def clear(self) -> None:
        """Clear all state values"""
        self._states.clear()


# Global state manager instance
manager = StateManager()
