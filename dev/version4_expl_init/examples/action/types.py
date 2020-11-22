import abc
from typing import Any, Dict

from dev.version4_expl_init.bases import Component


class DataContainerT(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_dict(cls, params: Dict[str, Any]) -> "DataContainerT":
        ...

    @abc.abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        ...


class RunnerT(Component, abc.ABC):
    @abc.abstractmethod
    def run(self, data: DataContainerT) -> DataContainerT:
        ...


class ValidatorT(Component, abc.ABC):
    @abc.abstractmethod
    def validate(self, data: DataContainerT) -> bool:
        ...


class ExecutorT(Component, abc.ABC):
    @abc.abstractmethod
    def execute(self, **kwargs) -> Any:
        ...
