"""Performance monitoring utilities"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import psutil

from pepperpy.core.exceptions import PepperPyError


class PerformanceError(PepperPyError):
    """Performance monitoring error"""


@dataclass
class ResourceUsage:
    """System resource usage information"""

    cpu_percent: float
    memory_percent: float
    disk_usage: dict[str, float]
    network_io: dict[str, int]
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


class PerformanceMonitor:
    """System performance monitor"""

    def __init__(self):
        self._process = psutil.Process()
        self._last_usage: ResourceUsage | None = None

    def get_resource_usage(self) -> ResourceUsage:
        """
        Get current resource usage

        Returns:
            ResourceUsage: Current resource usage information

        """
        try:
            # Get CPU and memory usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_percent = psutil.virtual_memory().percent

            # Get disk usage for all mounted partitions
            disk_usage = {
                partition.mountpoint: psutil.disk_usage(partition.mountpoint).percent
                for partition in psutil.disk_partitions()
                if partition.fstype
            }

            # Get network I/O counters
            net_io = psutil.net_io_counters()
            network_io = {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
            }

            usage = ResourceUsage(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_usage=disk_usage,
                network_io=network_io,
            )

            self._last_usage = usage
            return usage

        except Exception as e:
            raise PerformanceError(f"Failed to get resource usage: {e!s}", cause=e)

    def get_process_info(self) -> dict[str, Any]:
        """
        Get current process information

        Returns:
            Dict[str, Any]: Process information

        """
        try:
            return {
                "pid": self._process.pid,
                "cpu_percent": self._process.cpu_percent(),
                "memory_percent": self._process.memory_percent(),
                "threads": len(self._process.threads()),
                "open_files": len(self._process.open_files()),
                "connections": len(self._process.connections()),
            }
        except Exception as e:
            raise PerformanceError(f"Failed to get process info: {e!s}", cause=e)

    @property
    def last_usage(self) -> ResourceUsage | None:
        """Get last recorded resource usage"""
        return self._last_usage


# Global performance monitor instance
monitor = PerformanceMonitor()
