"""LLM configuration"""

from abc import ABC
from dataclasses import asdict, dataclass
from typing import Any, Literal

ProviderType = Literal["openai", "openrouter", "stackspot"]


@dataclass
class BaseConfig(ABC):
    """Base configuration interface"""

    provider: ProviderType
    api_key: str
    model: str

    def __post_init__(self) -> None:
        """Validate configuration"""
        if not self.api_key:
            raise ValueError("API key is required")
        if not self.provider:
            raise ValueError("Provider is required")

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary"""
        return asdict(self)


@dataclass
class OpenAIConfig(BaseConfig):
    """OpenAI specific configuration"""

    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    api_base: str | None = None

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        api_base: str | None = None,
    ) -> None:
        super().__init__(provider="openai", api_key=api_key, model=model)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.api_base = api_base


@dataclass
class OpenRouterConfig(BaseConfig):
    """OpenRouter specific configuration"""

    base_url: str = "https://openrouter.ai/api/v1"
    site_url: str | None = None
    site_name: str | None = None
    timeout: float = 60.0
    max_retries: int = 2
    temperature: float = 0.7

    def __init__(
        self,
        api_key: str,
        model: str = "anthropic/claude-3-sonnet",
        base_url: str = "https://openrouter.ai/api/v1",
        site_url: str | None = None,
        site_name: str | None = None,
        timeout: float = 60.0,
        max_retries: int = 2,
        temperature: float = 0.7,
    ) -> None:
        if not api_key:
            raise ValueError("OpenRouter API key is required")
        if not api_key.startswith("sk-"):
            raise ValueError("Invalid OpenRouter API key format. Key should start with 'sk-'")
        if len(api_key) < 20:
            raise ValueError("OpenRouter API key seems too short")

        super().__init__(provider="openrouter", api_key=api_key, model=model)
        self.base_url = base_url.rstrip("/")
        self.site_url = site_url
        self.site_name = site_name
        self.timeout = timeout
        self.max_retries = max_retries
        self.temperature = temperature


@dataclass
class StackSpotConfig(BaseConfig):
    """StackSpot specific configuration"""

    account_slug: str
    client_id: str
    client_key: str
    qc_slug: str
    base_url: str = "https://genai-code-buddy-api.stackspot.com/v1"
    auth_url: str = "https://idm.stackspot.com"

    def __init__(
        self,
        account_slug: str,
        client_id: str,
        client_key: str,
        qc_slug: str,
        model: str = "stackspot-ai",
        base_url: str = "https://genai-code-buddy-api.stackspot.com/v1",
        auth_url: str = "https://idm.stackspot.com",
    ) -> None:
        if not all([account_slug, client_id, client_key, qc_slug]):
            raise ValueError("All StackSpot credentials are required")

        super().__init__(provider="stackspot", api_key=client_key, model=model)
        self.account_slug = account_slug
        self.client_id = client_id
        self.client_key = client_key
        self.qc_slug = qc_slug
        self.base_url = base_url
        self.auth_url = auth_url
