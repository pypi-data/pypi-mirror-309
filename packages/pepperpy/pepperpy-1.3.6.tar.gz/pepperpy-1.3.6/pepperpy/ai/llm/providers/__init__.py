"""LLM providers"""

from .base import BaseLLMProvider
from .openrouter import OpenRouterConfig, OpenRouterProvider

__all__ = [
    "BaseLLMProvider",
    "OpenRouterConfig",
    "OpenRouterProvider",
]

import importlib.util

if importlib.util.find_spec(".openai", __package__):
    from .openai import OpenAIConfig, OpenAIProvider  # noqa: F401

    HAS_OPENAI = True
    __all__.extend(["OpenAIConfig", "OpenAIProvider"])
else:
    HAS_OPENAI = False
