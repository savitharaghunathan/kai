from dataclasses import dataclass, field
from pathlib import Path

from opentelemetry import trace

from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agent.maven_compiler_fix.agent import MavenCompilerAgent
from kai.reactive_codeplanner.agent.maven_compiler_fix.api import (
    MavenCompilerAgentRequest,
    MavenCompilerAgentResult,
)
from kai.reactive_codeplanner.task_manager.api import Task, TaskResult
from kai.reactive_codeplanner.task_runner.api import TaskRunner
from kai.reactive_codeplanner.task_runner.compiler.maven_validator import (
    AccessControlError,
    AnnotationError,
    BuildError,
    DependencyResolutionError,
    MavenCompilerError,
    OtherError,
    SymbolNotFoundError,
    SyntaxError,
    TypeMismatchError,
)
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager
from kai.reactive_codeplanner.vfs.spawning_result import SpawningResult

logger = get_logger(__name__)
tracer = trace.get_tracer("maven_compile_task_runner")


@dataclass
class MavenCompilerLLMResponse(SpawningResult):
    reasoning: str
    java_file: str
    additional_information: str
    file_path: str = ""
    input_file: str = ""
    input_errors: list[str] = field(default_factory=list)


class MavenCompilerTaskRunner(TaskRunner):
    """This agent is responsible for taking a set of maven compiler issues and solving.

    For a given file it will asking LLM's for the changes that are needed for the at whole file
    returning the results.
    """

    handled_type = (
        BuildError,
        SyntaxError,
        TypeMismatchError,
        AnnotationError,
        AccessControlError,
        OtherError,
        DependencyResolutionError,
        SymbolNotFoundError,
    )

    def __init__(self, agent: MavenCompilerAgent) -> None:
        self.agent = agent

    async def refine_task(self, errors: list[str]) -> None:
        """We currently do not refine the tasks"""
        return None

    async def can_handle_error(self, errors: list[str]) -> bool:
        """We currently do not know if we can handle errors"""
        return False

    async def can_handle_task(self, task: Task) -> bool:
        """Will determine if the task if a MavenCompilerError, and if we can handle these issues."""
        return isinstance(task, self.handled_type)

    @tracer.start_as_current_span("maven_execute_task")
    async def execute_task(self, rcm: RepoContextManager, task: Task) -> TaskResult:
        """This will be responsible for getting the full file from LLM and updating the file on disk"""

        # convert the task to the MavenCompilerError
        if not isinstance(task, MavenCompilerError):
            return TaskResult(encountered_errors=[], modified_files=[], summary="")

        with open(task.file) as f:
            src_file_contents = f.read()

        result = await self.agent.execute(
            MavenCompilerAgentRequest(
                file_path=Path(task.file),
                task=task,
                file_contents=src_file_contents,
                line_number=task.line,
                message=task.compiler_error_message(),
                background=task.background(),
            )
        )

        if not isinstance(result, MavenCompilerAgentResult):
            return TaskResult(encountered_errors=[], modified_files=[], summary="")

        if result.updated_file_contents is None:
            return TaskResult(encountered_errors=[], modified_files=[], summary="")

        # rewrite the file, based on the java file returned
        with open(task.file, "w") as f:
            f.write(result.updated_file_contents.lstrip())

        rcm.commit(f"MavenCompilerTaskRunner changed file {str(task.file)}", result)

        return TaskResult(
            modified_files=[Path(task.file)],
            encountered_errors=[],
            summary=result.reasoning or "",
        )
