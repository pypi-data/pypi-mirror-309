"""LLM provider factory"""

from typing import Any, Union, cast

from .config import (
    BaseConfig,
    OpenAIConfig,
    OpenRouterConfig,
    ProviderType,
    StackSpotConfig,
)
from .exceptions import ConfigurationError
from .providers.base import BaseLLMProvider
from .providers.openai import OpenAIProvider
from .providers.openrouter import OpenRouterProvider
from .providers.stackspot import StackSpotProvider

ProviderConfig = Union[OpenAIConfig, OpenRouterConfig, StackSpotConfig]


class ProviderFactory:
    """Factory for LLM providers"""

    _providers: dict[
        ProviderType, tuple[type[BaseLLMProvider[Any]], type[BaseConfig]],
    ] = {
        "openai": (OpenAIProvider, OpenAIConfig),
        "openrouter": (OpenRouterProvider, OpenRouterConfig),
        "stackspot": (StackSpotProvider, StackSpotConfig),
    }

    @classmethod
    def get_provider(
        cls, provider_type: ProviderType, config: ProviderConfig | None = None,
    ) -> BaseLLMProvider[Any]:
        """Get LLM provider instance"""
        if provider_type not in cls._providers:
            raise ConfigurationError(f"Unknown provider type: {provider_type}")

        provider_class, config_class = cls._providers[provider_type]

        if config is None:
            raise ConfigurationError("Provider configuration is required")

        if not isinstance(config, config_class):
            raise ConfigurationError(
                f"Invalid configuration type for provider {provider_type}. "
                f"Expected {config_class.__name__}, got {type(config).__name__}",
            )

        provider = cast(BaseLLMProvider[Any], provider_class(config=config))
        return provider


# Convenience function
def get_provider(
    provider_type: ProviderType, config: ProviderConfig | None = None,
) -> BaseLLMProvider[Any]:
    """Get LLM provider instance"""
    return ProviderFactory.get_provider(provider_type, config)
