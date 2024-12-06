"""Agent team management implementation"""

import asyncio

from ....console import Console
from ...types import AIResponse, Message
from ..config import TeamConfig
from ..types import ReviewResult, TaskPlan, TaskResult
from .base import AutoGenAgent


class AgentTeam:
    """Manages a team of collaborative agents"""

    def __init__(self, agents: list[AutoGenAgent], config: TeamConfig | None = None):
        self.agents = {agent.name: agent for agent in agents}
        self.config = config or TeamConfig()
        self.console = Console()
        self._validate_team()

    def _validate_team(self) -> None:
        """Validate team composition and roles"""
        required_roles = {"planner", "executor", "critic"}
        team_roles = {agent.role for agent in self.agents.values()}

        if not required_roles.issubset(team_roles):
            missing = required_roles - team_roles
            raise ValueError(f"Missing required roles: {missing}")

    async def execute_task(self, task: str) -> TaskResult:
        """Execute task using the agent team"""
        try:
            # 1. Plan task
            plan = await self._get_plan(task)
            self.console.info(f"📋 Created plan with {len(plan.steps)} steps")

            # 2. Execute steps
            results = []
            for step in plan.steps:
                try:
                    self.console.info(f"🔄 Executing step: {step[:100]}...")
                    result = await self._execute_step(step)
                    results.append(result)

                    # 3. Review result
                    review = await self._review_result(result)
                    if not review.approved:
                        self.console.warning(f"⚠️ Review failed: {review.feedback}")
                        # Handle revision with retry logic
                        max_retries = 3
                        for retry in range(max_retries):
                            try:
                                self.console.info(
                                    f"🔄 Attempting revision (try {retry + 1}/{max_retries})"
                                )
                                revised_result = await self._revise_task(step, review.feedback)
                                results[-1] = revised_result
                                # Check if revision passed review
                                review = await self._review_result(revised_result)
                                if review.approved:
                                    self.console.success("✅ Revision approved")
                                    break
                            except Exception as e:
                                self.console.warning(
                                    f"⚠️ Revision attempt {retry + 1} failed: {str(e)}"
                                )
                                if retry == max_retries - 1:
                                    raise
                                await asyncio.sleep(1)  # Brief delay before retry
                    else:
                        self.console.success("✅ Review passed")

                except Exception as step_error:
                    self.console.error(f"❌ Step execution failed: {str(step_error)}")
                    if len(results) < 2:  # If we haven't made much progress, fail the task
                        raise
                    # Otherwise, try to continue with next step
                    continue

            # 4. Compile final result
            return self._compile_results(task, results)

        except Exception as e:
            self.console.error(f"❌ Task execution failed: {str(e)}")
            # Return failed result instead of raising
            return TaskResult(
                success=False,
                output=f"Task failed: {str(e)}",
                steps=[{"content": str(e), "metadata": {"error": True}}],
            )

    async def _get_plan(self, task: str) -> TaskPlan:
        """Get task execution plan from planner"""
        try:
            planner = self._get_agent_by_role("planner")
            prompt = f"""Create a detailed step-by-step plan for the following task:

Task: {task}

Requirements:
1. Break down the task into clear, actionable steps
2. Each step should be focused on a single aspect
3. Include validation and testing steps
4. Consider error handling and edge cases

Format your response as a numbered list of steps.
"""
            response = await planner.send(prompt)
            return self._parse_plan(response)
        except Exception as e:
            self.console.error(f"❌ Planning failed: {str(e)}")
            raise

    async def _execute_step(self, step: str) -> AIResponse:
        """Execute single step using appropriate agent"""
        executor = self._get_agent_by_role("executor")
        prompt = f"""Implement the following development step:

Step: {step}

Requirements:
1. Provide complete, working code
2. Include error handling
3. Add clear comments
4. Consider edge cases
5. Follow Python best practices

Format your response with clear sections for:
- Implementation
- Error Handling
- Usage Example
"""
        return await executor.send(prompt)

    async def _review_result(self, result: AIResponse) -> ReviewResult:
        """Review step result"""
        critic = self._get_agent_by_role("critic")
        prompt = f"""Review the following implementation:

{result.content}

Review Criteria:
1. Code Quality and Style
2. Error Handling
3. Performance
4. Security
5. Best Practices

Format your response with:
- A clear APPROVED or NEEDS_REVISION status at the start
- Specific issues found (if any)
- Suggested improvements
"""
        response = await critic.send(prompt)
        return self._parse_review(response)

    async def _revise_task(self, task: str, feedback: str) -> AIResponse:
        """Revise task based on feedback"""
        executor = self._get_agent_by_role("executor")
        prompt = f"""Revise the implementation based on the following feedback:

Original Task:
{task}

Feedback Received:
{feedback}

Requirements for Revision:
1. Address each point in the feedback
2. Maintain or improve existing functionality
3. Follow best practices
4. Include error handling
5. Add clear comments

Format your response with:
- Summary of changes
- Updated implementation
- Explanation of improvements
"""
        return await executor.send(prompt)

    def _parse_plan(self, response: AIResponse) -> TaskPlan:
        """Parse planning response into structured plan"""
        # Implementar lógica de parsing do plano
        steps = [
            step.strip()
            for step in response.content.split("\n")
            if step.strip() and not step.startswith("#")
        ]
        return TaskPlan(steps=steps)

    def _parse_review(self, response: AIResponse) -> ReviewResult:
        """Parse review response into structured result"""
        content = response.content.lower()

        # Análise mais robusta do feedback
        approved = (
            "approved" in content
            or "passed" in content
            or "looks good" in content
            or "well implemented" in content
        )

        # Extrair sugestões de mudança
        changes = []
        for line in response.content.split("\n"):
            line = line.strip()
            if line and (
                line.startswith("-")
                or line.startswith("*")
                or "suggestion:" in line.lower()
                or "improve:" in line.lower()
            ):
                changes.append(line)

        return ReviewResult(approved=approved, feedback=response.content, changes_required=changes)

    def _compile_results(self, task: str, results: list[AIResponse]) -> TaskResult:
        """Compile individual results into final result"""
        # Combinar resultados em um resultado final
        combined_content = "\n\n".join(r.content for r in results)

        return TaskResult(
            success=True,
            output=combined_content,
            steps=[{"content": r.content, "metadata": r.metadata} for r in results],
        )

    def _get_agent_by_role(self, role: str) -> AutoGenAgent:
        """Get agent by role"""
        for agent in self.agents.values():
            if agent.role == role:
                return agent
        raise ValueError(f"No agent found for role: {role}")

    def broadcast(self, message: str) -> None:
        """Broadcast message to all agents"""
        for agent in self.agents.values():
            self.console.info(f"📢 Broadcasting to {agent.name}: {message}")
            agent.add_to_context(Message(content=message, sender="system"))

    def get_agent(self, name: str) -> AutoGenAgent | None:
        """Get agent by name"""
        return self.agents.get(name)

    def add_agent(self, agent: AutoGenAgent) -> None:
        """Add new agent to team"""
        self.agents[agent.name] = agent
        self._validate_team()

    def remove_agent(self, name: str) -> None:
        """Remove agent from team"""
        if name in self.agents:
            del self.agents[name]
            self._validate_team()
