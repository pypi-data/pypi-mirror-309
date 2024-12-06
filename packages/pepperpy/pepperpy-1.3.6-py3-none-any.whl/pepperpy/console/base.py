"""Base console functionality"""

from typing import Any

from .config import ConsoleConfig


class Console:
    """Console interface for terminal interactions"""

    def __init__(self, config: ConsoleConfig | None = None):
        self.config = config or ConsoleConfig()
        self._setup_console()

    def _setup_console(self) -> None:
        """Setup internal console implementation"""
        # Implementation will use rich internally but keeps it encapsulated
        from rich.console import Console as RichConsole

        self._console = RichConsole()

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print to console"""
        self._console.print(*args, **kwargs)

    def clear(self) -> None:
        """Clear console"""
        self._console.clear()

    # ... outros métodos do Console original
