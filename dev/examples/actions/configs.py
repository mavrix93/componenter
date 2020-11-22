from typing import Callable, Any, List

from componenter.component import ComponentConfig, Components
from dev.examples.actions.types import IExecutor, IRunner


class MethodExecutorConfig(ComponentConfig):
    method: Callable[..., Any]


class MethodValidationExecutorConfig(ComponentConfig):
    method: Callable[..., bool]


class RunnerComponents(Components):
    executor: IExecutor


class RunnerConfig(ComponentConfig):
    name: str


class ExecutionChainComponents(Components):
    runners: List[IRunner]
