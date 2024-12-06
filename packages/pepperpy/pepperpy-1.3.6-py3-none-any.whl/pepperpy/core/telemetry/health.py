"""Health check utilities"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Protocol, runtime_checkable

from pepperpy.core.exceptions import PepperPyError


class HealthError(PepperPyError):
    """Health check error"""


class Status(Enum):
    """Health check status"""

    UP = "up"
    DOWN = "down"
    DEGRADED = "degraded"


@runtime_checkable
class HealthCheck(Protocol):
    """Health check protocol"""

    name: str
    description: str

    def check(self) -> Status: ...


@dataclass
class HealthResult:
    """Health check result"""

    status: Status
    timestamp: datetime = field(default_factory=datetime.now)
    details: dict[str, Any] = field(default_factory=dict)


class HealthMonitor:
    """System health monitor"""

    def __init__(self):
        self._checks: dict[str, HealthCheck] = {}
        self._results: dict[str, HealthResult] = {}

    def register_check(self, check: HealthCheck) -> None:
        """
        Register health check

        Args:
            check: Health check to register

        """
        self._checks[check.name] = check

    def remove_check(self, name: str) -> None:
        """
        Remove health check

        Args:
            name: Name of check to remove

        """
        if name in self._checks:
            del self._checks[name]
            if name in self._results:
                del self._results[name]

    def check_health(self, name: str | None = None) -> dict[str, HealthResult]:
        """
        Run health checks

        Args:
            name: Optional name of specific check to run

        Returns:
            Dict[str, HealthResult]: Health check results

        """
        try:
            if name:
                if name not in self._checks:
                    raise HealthError(f"Health check not found: {name}")
                check = self._checks[name]
                result = HealthResult(status=check.check())
                self._results[name] = result
                return {name: result}

            results = {}
            for check_name, check in self._checks.items():
                try:
                    status = check.check()
                    result = HealthResult(status=status)
                except Exception as e:
                    result = HealthResult(
                        status=Status.DOWN,
                        details={"error": str(e)},
                    )
                results[check_name] = result
                self._results[check_name] = result

            return results

        except Exception as e:
            raise HealthError(f"Health check failed: {e!s}", cause=e)

    def get_results(self, name: str | None = None) -> dict[str, HealthResult]:
        """
        Get health check results

        Args:
            name: Optional name of specific check result to get

        Returns:
            Dict[str, HealthResult]: Health check results

        """
        if name:
            if name not in self._results:
                raise HealthError(f"Health check result not found: {name}")
            return {name: self._results[name]}
        return self._results.copy()


# Global health monitor instance
monitor = HealthMonitor()
