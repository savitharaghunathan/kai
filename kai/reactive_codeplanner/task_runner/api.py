from abc import ABC, abstractmethod

from kai.reactive_codeplanner.task_manager.api import Task, TaskResult
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager


class TaskRunner(ABC):
    @abstractmethod
    async def can_handle_task(self, task: Task) -> bool:
        pass

    @abstractmethod
    async def execute_task(self, rcm: RepoContextManager, task: Task) -> TaskResult:
        pass

    @abstractmethod
    async def refine_task(self, errors: list[str]) -> None:
        # Knows that it's the refine step so that it might not spawn as much
        # stuff.
        pass

    @abstractmethod
    async def can_handle_error(self, errors: list[str]) -> bool:
        pass
