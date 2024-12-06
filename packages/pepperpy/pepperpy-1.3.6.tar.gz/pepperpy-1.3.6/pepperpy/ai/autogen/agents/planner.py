"""Planning specialist agent implementation"""

from typing import Any

from ...client import AIClient
from ...types import AIResponse, UsageInfo
from ..types import Message
from .base import AutoGenAgent


class PlannerAgent(AutoGenAgent):
    """Agent specialized in task planning and architecture"""

    def __init__(
        self,
        name: str = "Technical Architect",
        client: AIClient | None = None,
        **kwargs: Any,
    ):
        super().__init__(
            name=name,
            role="planner",
            instructions=kwargs.pop("instructions", ""),
            client=client,
            **kwargs,
        )

    async def _generate_response(self, message: Message) -> AIResponse:
        """Generate planning response"""
        if not self.client:
            raise ValueError("Client is required for generating responses")

        prompt = f"""As a technical architect, analyze and plan for:

{message.content}

Provide a detailed plan considering:
1. Technical requirements
2. Implementation steps
3. Potential challenges
4. Best practices to follow
5. Success criteria
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

    async def plan_task(self, task: str) -> AIResponse:
        """Create detailed plan for task"""
        return await self.send(
            f"""Create a detailed plan for this task:

{task}

Break it down into:
1. Clear objectives
2. Implementation steps
3. Technical requirements
4. Quality criteria
5. Potential challenges
""",
        )
