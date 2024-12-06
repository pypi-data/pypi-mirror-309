"""OpenAI LLM provider implementation"""

from collections.abc import AsyncIterator
from typing import cast

import openai
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionAssistantMessageParam,
    ChatCompletionChunk,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from pepperpy.ai.llm.exceptions import ProviderError
from pepperpy.ai.llm.types import LLMConfig, LLMResponse, Message

from .base import BaseLLMProvider


class OpenAIConfig(LLMConfig):
    """OpenAI provider configuration"""

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
        if not api_key:
            raise ValueError("OpenAI API key is required")

        super().__init__(provider="openai", api_key=api_key, model=model)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.api_base = api_base


class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider implementation"""

    def __init__(self, config: OpenAIConfig | None = None) -> None:
        if not config:
            raise ValueError("OpenAI configuration is required")

        self.config = config
        self._client = None

    async def initialize(self) -> None:
        """Initialize provider"""
        openai.api_key = self.config.api_key
        if self.config.api_base:
            openai.base_url = self.config.api_base
        self._client = openai.AsyncClient()

    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        if self._client:
            await self._client.close()
            self._client = None

    def _convert_messages(self, messages: list[Message]) -> list[ChatCompletionMessageParam]:
        """Convert messages to OpenAI format"""
        converted: list[ChatCompletionMessageParam] = []

        for msg in messages:
            if msg["role"] == "system":
                converted.append(
                    ChatCompletionSystemMessageParam(role="system", content=msg["content"]),
                )
            elif msg["role"] == "user":
                converted.append(
                    ChatCompletionUserMessageParam(role="user", content=msg["content"]),
                )
            elif msg["role"] == "assistant":
                converted.append(
                    ChatCompletionAssistantMessageParam(role="assistant", content=msg["content"]),
                )

        return converted

    async def complete(self, messages: list[Message]) -> LLMResponse:
        """Complete chat messages"""
        if not self._client:
            raise ProviderError("OpenAI client not initialized")

        try:
            response: ChatCompletion = await self._client.chat.completions.create(
                model=self.config.model,
                messages=self._convert_messages(messages),
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p,
                frequency_penalty=self.config.frequency_penalty,
                presence_penalty=self.config.presence_penalty,
            )

            content = response.choices[0].message.content
            if not content:
                raise ProviderError("Empty response from OpenAI")

            return LLMResponse(
                content=content,
                model=response.model,
                usage=(
                    {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                    }
                    if response.usage
                    else {}
                ),
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "system_fingerprint": response.system_fingerprint,
                },
            )
        except Exception as e:
            raise ProviderError("Failed to complete chat", cause=e)

    async def stream(self, messages: list[Message]) -> AsyncIterator[LLMResponse]:
        """Stream responses from OpenAI"""
        if not self._client:
            raise ProviderError("OpenAI client not initialized")

        try:
            stream = await self._client.chat.completions.create(
                model=self.config.model,
                messages=self._convert_messages(messages),
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p,
                frequency_penalty=self.config.frequency_penalty,
                presence_penalty=self.config.presence_penalty,
                stream=True,
            )

            async for chunk in stream:
                chunk = cast(ChatCompletionChunk, chunk)
                content = chunk.choices[0].delta.content
                if content:
                    yield LLMResponse(
                        content=content,
                        model=chunk.model,
                        usage={},  # Usage não disponível em chunks
                        metadata={
                            "finish_reason": chunk.choices[0].finish_reason,
                            "system_fingerprint": chunk.system_fingerprint,
                        },
                    )
        except Exception as e:
            raise ProviderError("Failed to stream responses", cause=e)
