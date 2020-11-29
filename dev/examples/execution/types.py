import abc
from typing import Protocol, TypeVar, Generic, NoReturn, List

from componenter.component import Components

TaskT = TypeVar("TaskT")
DataT = TypeVar("DataT")
ProcessedDataT = TypeVar("ProcessedDataT")


class ExecutorT(Generic[TaskT, DataT, ProcessedDataT], abc.ABC):
    @abc.abstractmethod
    def run(self, task: TaskT, data: List[DataT]) -> List[ProcessedDataT]:
        ...


class ResultParserT(Generic[DataT, ProcessedDataT], abc.ABC):
    @abc.abstractmethod
    def parse(self, result: DataT) -> ProcessedDataT:
        ...


class LoggerT(Generic[DataT], abc.ABC):
    @abc.abstractmethod
    def log(self, data: DataT) -> NoReturn:
        pass


class ExecutorComponents(Components):
    logger: LoggerT
    parser: ResultParserT


class TaskMethodComponents(Components):
    executor: ExecutorT
