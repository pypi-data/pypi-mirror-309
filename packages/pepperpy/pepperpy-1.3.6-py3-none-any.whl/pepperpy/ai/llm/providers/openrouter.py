"""OpenRouter LLM provider"""

import json
from typing import AsyncIterator

import httpx

from pepperpy.ai.llm.config import OpenRouterConfig
from pepperpy.ai.llm.exceptions import ProviderError
from pepperpy.ai.llm.types import LLMResponse, Message

from .base import BaseLLMProvider


class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter provider implementation"""

    def __init__(self, config: OpenRouterConfig) -> None:
        super().__init__()
        if not isinstance(config, OpenRouterConfig):
            raise ValueError("OpenRouter provider requires OpenRouterConfig")
        self.config = config
        self._client: httpx.AsyncClient | None = None

    async def initialize(self) -> None:
        """Initialize provider"""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "HTTP-Referer": self.config.site_url or "https://github.com/felipepimentel/pepperpy",
            "X-Title": self.config.site_name or "PepperPy",
        }
        self._client = httpx.AsyncClient(
            base_url="https://openrouter.ai/api/v1",
            headers=headers,
            timeout=self.config.timeout,
        )

    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def complete(self, messages: list[Message]) -> LLMResponse:
        """Complete chat messages"""
        if not self._client:
            raise ProviderError("Provider not initialized")

        if not messages:
            raise ValueError("At least one message is required")

        try:
            response = await self._client.post(
                "/chat/completions",
                json={
                    "model": self.config.model,
                    "messages": messages,
                },
            )
            response.raise_for_status()
            data = response.json()

            if not data.get("choices"):
                raise ProviderError("Invalid response from OpenRouter API")

            return LLMResponse(
                content=data["choices"][0]["message"]["content"],
                model=data["model"],
                usage=data.get("usage", {}),
                metadata={
                    "finish_reason": data["choices"][0].get("finish_reason"),
                    "model": data.get("model"),
                    "route": data.get("route"),
                },
            )
        except httpx.HTTPError as e:
            raise ProviderError(f"HTTP error: {e!s}", cause=e)
        except Exception as e:
            raise ProviderError(f"Failed to complete chat: {e!s}", cause=e)

    def stream(self, messages: list[Message]) -> AsyncIterator[LLMResponse]:
        """Stream chat completion"""
        if not self._client:
            raise ProviderError("Provider not initialized")

        if not messages:
            raise ValueError("At least one message is required")

        client = self._client

        async def stream_generator() -> AsyncIterator[LLMResponse]:
            try:
                response = await client.post(
                    "/chat/completions",
                    json={
                        "model": self.config.model,
                        "messages": messages,
                        "stream": True,
                    },
                    headers={"Accept": "text/event-stream"},
                )
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            if data["choices"][0]["delta"].get("content"):
                                yield LLMResponse(
                                    content=data["choices"][0]["delta"]["content"],
                                    model=data["model"],
                                    usage={},
                                    metadata=data,
                                )
                        except json.JSONDecodeError as e:
                            raise ProviderError(f"Invalid JSON response: {e!s}", cause=e)
            except httpx.HTTPError as e:
                raise ProviderError(f"HTTP error: {e!s}", cause=e)
            except Exception as e:
                raise ProviderError(f"Failed to stream chat: {e!s}", cause=e)

        return stream_generator()
