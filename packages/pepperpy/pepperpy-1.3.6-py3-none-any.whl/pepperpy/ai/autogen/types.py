"""AutoGen types and data structures"""

from dataclasses import dataclass, field
from typing import Any

from ..types import AIResponse, Message

__all__ = [
    "Message",
    "CodeReview",
    "TaskPlan",
    "TaskResult",
    "ReviewResult",
]


@dataclass
class CodeReview:
    """Code review result"""

    approved: bool
    feedback: str
    suggestions: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskPlan:
    """Task execution plan"""

    steps: list[str] = field(default_factory=list)
    dependencies: dict[str, list[str]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskResult:
    """Task execution result"""

    success: bool
    output: str | AIResponse
    steps: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReviewResult:
    """Review result"""

    approved: bool
    feedback: str
    changes_required: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
