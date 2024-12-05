from typing import AsyncGenerator, Callable, Union, Optional
import time
from .database import ComponentFactory, Component
from .datamodel import TeamResult, TaskResult, ComponentConfigInput
from autogen_agentchat.messages import InnerMessage, ChatMessage
from autogen_core.base import CancellationToken


class TeamManager:
    def __init__(self) -> None:
        self.component_factory = ComponentFactory()

    async def _create_team(
        self,
        team_config: ComponentConfigInput,
        input_func: Optional[Callable] = None
    ) -> Component:
        """Create team instance with common setup logic"""
        return await self.component_factory.load(
            team_config,
            input_func=input_func
        )

    def _create_result(self, task_result: TaskResult, start_time: float) -> TeamResult:
        """Create TeamResult with timing info"""
        return TeamResult(
            task_result=task_result,
            usage="",
            duration=time.time() - start_time
        )

    async def run_stream(
        self,
        task: str,
        team_config: ComponentConfigInput,
        input_func: Optional[Callable] = None,
        cancellation_token: Optional[CancellationToken] = None
    ) -> AsyncGenerator[Union[InnerMessage, ChatMessage, TaskResult], None]:
        """Stream the team's execution results"""
        start_time = time.time()

        try:
            team = await self._create_team(team_config, input_func)
            stream = team.run_stream(
                task=task,
                cancellation_token=cancellation_token
            )

            async for message in stream:
                if cancellation_token and cancellation_token.is_cancelled():
                    break

                if isinstance(message, TaskResult):
                    yield self._create_result(message, start_time)
                else:
                    yield message

        except Exception as e:
            raise e

    async def run(
        self,
        task: str,
        team_config: ComponentConfigInput,
        input_func: Optional[Callable] = None,
        cancellation_token: Optional[CancellationToken] = None
    ) -> TeamResult:
        """Original non-streaming run method with optional cancellation"""
        start_time = time.time()

        team = await self._create_team(team_config, input_func)
        result = await team.run(
            task=task,
            cancellation_token=cancellation_token
        )

        return self._create_result(result, start_time)
