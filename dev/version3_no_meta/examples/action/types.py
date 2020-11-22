import abc
from typing import Any, Dict

from dev.version3_no_meta import ComponentT, ComponentGenT


class DataContainerT(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_dict(cls, params: Dict[str, Any]) -> "DataContainerT":
        ...

    @abc.abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        ...


class RunnerT(ComponentT, abc.ABC):
    @abc.abstractmethod
    def run(self, data: DataContainerT) -> DataContainerT:
        ...


class ValidatorT(ComponentT, abc.ABC):
    @abc.abstractmethod
    def validate(self, data: DataContainerT) -> bool:
        ...


class ExecutorT(ComponentT[ComponentGenT], abc.ABC):
    @abc.abstractmethod
    def execute(self, **kwargs) -> Any:
        ...

    # @abc.abstractmethod
    # def unwrap(self, data: DataContainerT) -> Dict[str, Any]:
    #     ...
    #
    # @abc.abstractmethod
    # def wrap(self, result: Any) -> DataContainerT:
    #     ...
