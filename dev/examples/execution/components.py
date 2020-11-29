import abc
import asyncio
import json
from asyncio import AbstractEventLoop
from typing import Callable, NoReturn, Generic, TypeVar, Coroutine, Awaitable, List

from componenter.component import Component, Components, ComponentConfig
from dev.examples.execution.types import (
    ExecutorT,
    LoggerT,
    DataT,
    ResultParserT,
    ProcessedDataT,
    ExecutorComponents,
    TaskMethodComponents,
)


class PrintLogger(LoggerT, Component):
    def log(self, data: DataT) -> NoReturn:
        print(data)


class NoParsing(ResultParserT[DataT, DataT], Component):
    def parse(self, result: DataT) -> DataT:
        return result


class ToJsonParsing(ResultParserT[dict, str], Component):
    def parse(self, result: dict) -> str:
        return json.dumps(result)


class AsyncExecutor(
    Generic[DataT, ProcessedDataT],
    ExecutorT[Callable[[DataT], Awaitable[DataT]], DataT, ProcessedDataT],
    Component[ComponentConfig, ExecutorComponents],
    components=(LoggerT[DataT], ResultParserT[DataT, ProcessedDataT]),
):

    loop: AbstractEventLoop

    def run(self, task: Callable, data: List[DataT]) -> List[ProcessedDataT]:
        self[LoggerT].log({"event": "Starting", "data": data})
        return [
            self[ResultParserT].parse(r)
            for r in [self.loop.run_until_complete(asyncio.gather(*[task(d)])) for d in data]
        ]


class SyncExecutor(
    Generic[DataT, ProcessedDataT],
    ExecutorT[Callable[[DataT], DataT], DataT, ProcessedDataT],
    Component[ComponentConfig, ExecutorComponents],
    components=(LoggerT[DataT], ResultParserT[DataT, ProcessedDataT]),
):
    def run(self, task: Callable, data: List[DataT]) -> List[ProcessedDataT]:
        self[LoggerT].log({"event": "Starting", "data": data})
        return [self[ResultParserT].parse(task(d)) for d in data]


class TaskMethodExecutor(Generic[DataT, ProcessedDataT], Component[ComponentConfig, TaskMethodComponents], abc.ABC):
    def run(self, data: List[DataT]):
        return self[ExecutorT].run(data=data, task=self.task_method)

    @abc.abstractmethod
    def task_method(self, data: DataT) -> DataT:
        pass
