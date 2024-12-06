"""Executor agent implementation"""

from typing import Any

from ...client import AIClient
from ...types import AIResponse, UsageInfo
from ..types import Message
from .base import AutoGenAgent


class ExecutorAgent(AutoGenAgent):
    """Agent specialized in executing tasks and implementing solutions"""

    def __init__(
        self,
        name: str = "Implementation Expert",
        client: AIClient | None = None,
        **kwargs: Any,
    ):
        super().__init__(
            name=name,
            role="executor",
            instructions=kwargs.pop("instructions", ""),
            client=client,
            **kwargs,
        )

    async def _generate_response(self, message: Message) -> AIResponse:
        """Generate execution response"""
        if not self.client:
            raise ValueError("Client is required for generating responses")

        prompt = f"""As an implementation expert, execute this task:

{message.content}

Ensure:
1. Complete implementation
2. Error handling
3. Clear documentation
4. Edge case handling
5. Best practices
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
