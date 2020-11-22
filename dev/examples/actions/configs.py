from typing import NamedTuple, Callable, Any, List

from dev.examples.actions.types import IExecutor, IRunner


class MethodExecutorConfig(NamedTuple):
    method: Callable[..., Any]


class MethodValidationExecutorConfig(NamedTuple):
    method: Callable[..., bool]


class RunnerComponents(NamedTuple):
    executor: IExecutor


class RunnerConfig(NamedTuple):
    name: str


class ExecutionChainComponents(NamedTuple):
    runners: List[IRunner]
