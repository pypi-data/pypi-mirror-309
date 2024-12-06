"""AutoGen configuration"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentConfig:
    """Configuration for individual agents"""

    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    stop_sequences: list[str] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_llm_config(self) -> dict[str, Any]:
        """Convert to LLM configuration"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": self.stop_sequences,
        }


@dataclass
class TeamConfig:
    """Configuration for agent teams"""

    max_iterations: int = 10
    timeout: float = 300.0  # 5 minutes
    parallel_execution: bool = True
    review_required: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
