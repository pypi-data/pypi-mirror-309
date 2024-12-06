"""Task scheduling and management"""

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, TypeVar

from pepperpy.core.exceptions import PepperPyError

T = TypeVar("T")


class TaskError(PepperPyError):
    """Task-related error"""


@dataclass
class Task:
    """Task configuration"""

    name: str
    func: Callable[..., Awaitable[Any]]
    interval: timedelta
    last_run: datetime | None = None
    next_run: datetime | None = None
    running: bool = False
    args: tuple = ()
    kwargs: dict[str, Any] = field(default_factory=dict)


class TaskScheduler:
    """Task scheduler for managing periodic tasks"""

    def __init__(self):
        self._tasks: dict[str, Task] = {}
        self._running: dict[str, Task] = {}
        self._stop = False

    def add_task(
        self,
        name: str,
        func: Callable[..., Awaitable[T]],
        interval: timedelta,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Add task to scheduler

        Args:
            name: Task name
            func: Task function
            interval: Task interval
            args: Task arguments
            kwargs: Task keyword arguments

        """
        if name in self._tasks:
            raise TaskError(f"Task {name} already exists")

        task = Task(
            name=name,
            func=func,
            interval=interval,
            args=args,
            kwargs=kwargs,
            next_run=datetime.now(),
        )
        self._tasks[name] = task

    def remove_task(self, name: str) -> None:
        """
        Remove task from scheduler

        Args:
            name: Task name

        """
        if name not in self._tasks:
            raise TaskError(f"Task {name} not found")

        if name in self._running:
            raise TaskError(f"Task {name} is running")

        del self._tasks[name]

    async def start(self) -> None:
        """Start task scheduler"""
        self._stop = False
        while not self._stop:
            now = datetime.now()
            for task in self._tasks.values():
                if task.next_run and now >= task.next_run and not task.running:
                    await self._run_task(task)
            await asyncio.sleep(1)

    def stop(self) -> None:
        """Stop task scheduler"""
        self._stop = True
        self._running.clear()

    async def _run_task(self, task: Task) -> None:
        """
        Run task

        Args:
            task: Task to run

        """
        try:
            task.running = True
            self._running[task.name] = task
            await task.func(*task.args, **task.kwargs)
            task.last_run = datetime.now()
            task.next_run = task.last_run + task.interval
        except Exception as e:
            raise TaskError(f"Task {task.name} failed: {e!s}", cause=e)
        finally:
            task.running = False
            if task.name in self._running:
                del self._running[task.name]


# Global task scheduler instance
scheduler = TaskScheduler()
