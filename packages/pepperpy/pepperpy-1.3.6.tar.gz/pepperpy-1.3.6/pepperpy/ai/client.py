"""AI client implementation"""

import os
from collections.abc import AsyncIterator, Sequence
from typing import Any, ClassVar, cast

from dotenv import load_dotenv

from .chat.types import ChatRole
from .exceptions import AIError
from .llm import LLMClient, Message, OpenRouterConfig
from .types import AIResponse, UsageInfo

load_dotenv()


class AIConfig:
    """Configuration for AI client"""

    DEFAULT_SITE_URL: ClassVar[str] = "https://github.com/felipepimentel/pepperpy"
    DEFAULT_SITE_NAME: ClassVar[str] = "PepperPy"

    def __init__(
        self,
        api_key: str,
        model: str,
        site_url: str = DEFAULT_SITE_URL,
        site_name: str = DEFAULT_SITE_NAME,
    ):
        self.api_key = api_key
        self.model = model
        self.site_url = site_url
        self.site_name = site_name

    @classmethod
    def from_env(cls) -> "AIConfig":
        """Create configuration from environment variables"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise AIError("OPENROUTER_API_KEY environment variable is required")

        return cls(
            api_key=api_key,
            model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4"),
            site_url=os.getenv("SITE_URL", cls.DEFAULT_SITE_URL),
            site_name=os.getenv("SITE_NAME", cls.DEFAULT_SITE_NAME),
        )

    def to_llm_config(self) -> OpenRouterConfig:
        """Convert to LLM configuration"""
        return OpenRouterConfig(
            api_key=self.api_key,
            model=self.model,
            site_url=self.site_url,
            site_name=self.site_name,
        )


class AIClient:
    """High-level AI client interface"""

    def __init__(self, config: AIConfig | None = None):
        """Initialize AI client with optional config"""
        self.config = config or AIConfig.from_env()
        self._client = LLMClient(self.config.to_llm_config())
        self.model = self.config.model

    @classmethod
    async def create(cls) -> "AIClient":
        """Create client from environment"""
        config = AIConfig.from_env()
        client = cls(config)
        await client.initialize()
        return client

    async def initialize(self) -> None:
        """Initialize client"""
        await self._client.initialize()

    async def cleanup(self) -> None:
        """Cleanup resources"""
        await self._client.cleanup()

    async def ask(self, prompt: str) -> AIResponse:
        """Send prompt to AI model and get response"""
        try:
            response = await self._client.complete([Message(role="user", content=prompt)])

            usage = UsageInfo(
                prompt_tokens=len(prompt.split()),
                completion_tokens=len(response.content.split()),
                total_tokens=len(prompt.split()) + len(response.content.split()),
            )

            return AIResponse(
                content=response.content, model=self.model, usage=usage, metadata=response.metadata,
            )
        except Exception as e:
            raise AIError(f"Failed to get response: {e!s}", cause=e)

    async def complete(self, messages: Sequence[dict[str, str]]) -> AIResponse:
        """
        Complete chat messages

        Args:
            messages: List of messages in the format {"role": str, "content": str}

        Returns:
            AIResponse: The completion response

        """
        try:
            # Validate and convert roles
            llm_messages = []
            for msg in messages:
                role = msg["role"]
                if role not in ("system", "user", "assistant"):
                    raise AIError(f"Invalid role: {role}")
                llm_messages.append(
                    Message(
                        role=cast(ChatRole, role),
                        content=msg["content"],
                    ),
                )

            response = await self._client.complete(llm_messages)
            usage = UsageInfo(
                prompt_tokens=sum(len(msg["content"].split()) for msg in messages),
                completion_tokens=len(response.content.split()),
                total_tokens=sum(len(msg["content"].split()) for msg in messages)
                + len(response.content.split()),
            )

            return AIResponse(
                content=response.content,
                model=self.model,
                usage=usage,
                metadata=response.metadata,
            )
        except Exception as e:
            raise AIError(f"Completion failed: {e!s}", cause=e)

    async def stream(self, messages: Sequence[dict[str, str]]) -> AsyncIterator[AIResponse]:
        """
        Stream chat completions

        Args:
            messages: List of messages in the format {"role": str, "content": str}

        Yields:
            AIResponse: The streamed response chunks

        """
        try:
            # Validate and convert roles
            llm_messages = []
            for msg in messages:
                role = msg["role"]
                if role not in ("system", "user", "assistant"):
                    raise AIError(f"Invalid role: {role}")
                llm_messages.append(
                    Message(
                        role=cast(ChatRole, role),
                        content=msg["content"],
                    ),
                )

            async for response in self._client.stream(llm_messages):
                yield AIResponse(
                    content=response.content,
                    model=self.model,
                    usage=UsageInfo(
                        prompt_tokens=sum(len(msg["content"].split()) for msg in messages),
                        completion_tokens=len(response.content.split()),
                        total_tokens=sum(len(msg["content"].split()) for msg in messages)
                        + len(response.content.split()),
                    ),
                    metadata=response.metadata,
                )
        except Exception as e:
            raise AIError(f"Streaming failed: {e!s}", cause=e)

    async def __aenter__(self) -> "AIClient":
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit"""
        await self.cleanup()
