import abc
import asyncio
import json
from asyncio import AbstractEventLoop, get_event_loop
from typing import Callable, NoReturn, Generic, Awaitable, List, Tuple

from componenter.component import Component, ComponentWithoutComponents
from dev.examples.execution.types import (
    ExecutorT,
    LoggerT,
    DataT,
    ResultParserT,
    ProcessedDataT,
    EventLoopProviderT,
)


class PrintLogger(LoggerT[dict], ComponentWithoutComponents):
    def log(self, data: dict) -> NoReturn:
        print(data)


class NoParsing(ResultParserT[DataT, DataT], ComponentWithoutComponents):
    def parse(self, result: DataT) -> DataT:
        return result


class ToJsonParsing(ResultParserT[dict, str], ComponentWithoutComponents):
    def parse(self, result: dict) -> str:
        return json.dumps(result)


class AsyncExecutor(
    Generic[DataT, ProcessedDataT],
    ExecutorT[Callable[[DataT], Awaitable[DataT]], DataT, ProcessedDataT],
    Component[Tuple[LoggerT[DataT], ResultParserT[DataT, ProcessedDataT], EventLoopProviderT]],
):
    def run(self, task: Callable, data: List[DataT]) -> List[ProcessedDataT]:
        self[LoggerT].log({"event": "Starting", "data": data})
        loop = self[EventLoopProviderT].get_event_loop()
        return [
            self[ResultParserT].parse(r) for r in [loop.run_until_complete(asyncio.gather(*[task(d)])) for d in data]
        ]


class SyncExecutor(
    Generic[DataT, ProcessedDataT],
    ExecutorT[Callable[[DataT], DataT], DataT, ProcessedDataT],
    Component[Tuple[LoggerT[DataT], ResultParserT[DataT, ProcessedDataT]]],
):
    def run(self, task: Callable, data: List[DataT]) -> List[ProcessedDataT]:
        self[LoggerT].log({"event": "Starting", "data": data})
        return [self.components[1].parse(task(d)) for d in data]


class TaskMethodExecutor(Generic[DataT, ProcessedDataT], Component[Tuple[ExecutorT]], abc.ABC):
    def run(self, data: List[DataT]):
        return self[ExecutorT].run(data=data, task=self.task_method)

    @abc.abstractmethod
    def task_method(self, data: DataT) -> DataT:
        pass


class EventLoopProvider(EventLoopProviderT):
    def get_event_loop(self) -> AbstractEventLoop:
        return get_event_loop()
