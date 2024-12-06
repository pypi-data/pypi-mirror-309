"""Coding specialist agent implementation"""

from typing import Any

from ...client import AIClient
from ...types import AIResponse, UsageInfo
from ..types import Message
from .base import AutoGenAgent


class CoderAgent(AutoGenAgent):
    """Agent specialized in code generation and review"""

    def __init__(
        self,
        name: str = "Code Expert",
        client: AIClient | None = None,
        **kwargs: Any,
    ):
        super().__init__(
            name=name,
            role="coder",
            instructions=kwargs.pop("instructions", ""),
            client=client,
            **kwargs,
        )

    async def _generate_response(self, message: Message) -> AIResponse:
        """Generate coding response"""
        if not self.client:
            raise ValueError("Client is required for generating responses")

        prompt = f"""As a coding expert, implement a solution for:

{message.content}

Focus on:
1. Clean, efficient code
2. Best practices
3. Error handling
4. Documentation
5. Edge cases
"""
        response = await self.client.ask(prompt)
        return AIResponse(
            content=response.content,
            model=self.client.model,
            usage=UsageInfo(
                prompt_tokens=len(prompt.split()),
                completion_tokens=len(response.content.split()),
                total_tokens=len(prompt.split()) + len(response.content.split()),
            ),
        )
