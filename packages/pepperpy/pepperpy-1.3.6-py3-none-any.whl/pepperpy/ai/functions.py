"""High-level convenience functions for AI operations"""

from collections.abc import AsyncIterator, Sequence

from .client import AIClient
from .types import AIResponse


async def ask(prompt: str) -> AIResponse:
    """
    Send a single prompt and get response

    Args:
        prompt: The prompt to send

    Returns:
        AIResponse: The model's response

    """
    client = await AIClient.create()
    async with client:
        return await client.ask(prompt)


async def complete(messages: Sequence[dict[str, str]]) -> AIResponse:
    """
    Complete a sequence of chat messages

    Args:
        messages: List of messages in the format {"role": str, "content": str}

    Returns:
        AIResponse: The completion response

    """
    client = await AIClient.create()
    async with client:
        return await client.complete(messages)


async def stream(messages: Sequence[dict[str, str]]) -> AsyncIterator[AIResponse]:
    """
    Stream chat completions

    Args:
        messages: List of messages in the format {"role": str, "content": str}

    Yields:
        AIResponse: The streamed response chunks

    """
    client = await AIClient.create()
    async with client:
        async for response in client.stream(messages):
            yield response
