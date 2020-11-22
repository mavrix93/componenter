import abc
from typing import Any

from pydantic import BaseModel


class DataContainer(BaseModel):
    pass


class IRunner(abc.ABC):
    @abc.abstractmethod
    def run(self, data: DataContainer) -> DataContainer:
        ...


class IExecutor(abc.ABC):
    @abc.abstractmethod
    def execute(self, **kwargs) -> Any:
        ...


class IExecutionChain(abc.ABC):
    @abc.abstractmethod
    def run_chain(self, data: DataContainer) -> DataContainer:
        ...
