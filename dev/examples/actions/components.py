from typing import Any

from componenter.component import Component, ComponentConfigT, ComponentsT, Components, ComponentConfig
from dev.examples.actions.configs import (
    RunnerComponents,
    RunnerConfig,
    MethodExecutorConfig,
    MethodValidationExecutorConfig,
    ExecutionChainComponents,
)
from dev.examples.actions.types import IRunner, IExecutor, DataContainer, IExecutionChain


class Executor(Component[ComponentConfigT, ComponentsT], IExecutor):
    def execute(self, **kwargs) -> Any:
        pass


class MethodExecutor(Executor[MethodExecutorConfig, Components], IExecutor):
    def execute(self, **kwargs) -> Any:
        return self.config.method(**kwargs)


class ValidationExecutor(Executor[MethodValidationExecutorConfig, Components], IExecutor):
    def execute(self, **kwargs):
        if not self.config.method(**kwargs):
            raise ValueError("Validation failed for {} with {}".format(self.__class__, kwargs))


class NoChangeRunner(Component[RunnerConfig, RunnerComponents], IRunner):
    def run(self, data: DataContainer) -> DataContainer:
        self.components.executor.execute(**data.dict())
        return data


class ExecutionChain(Component[ComponentConfig, ExecutionChainComponents], IExecutionChain):
    def run_chain(self, data: DataContainer) -> DataContainer:
        for runner in self.components.runners:
            data = runner.run(data)
        return data
