from typing import Any, Dict, Type
import abc
from dev.version2.bases import Component
from dev.version2.examples import ExecutorT, DataContainerT


### Base


class Container(DataContainerT):
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @classmethod
    def from_dict(cls, params: Dict[str, Any]) -> "DataContainerT":
        return cls(params)

    def to_dict(self) -> Dict[str, Any]:
        return self.data


class Executor(ExecutorT, abc.ABC):
    PROVIDES: str
    DATA_CONTAINER: Type[DataContainerT]

    def run(self, data: DataContainerT) -> DataContainerT:
        return self.wrap(self.execute(**self.unwrap(data)))

    @abc.abstractmethod
    def execute(self, **kwargs) -> Any:
        pass

    def unwrap(self, data: DataContainerT) -> Dict[str, Any]:
        return data.to_dict()

    def wrap(self, result: Any) -> DataContainerT:
        return self.DATA_CONTAINER.from_dict({self.PROVIDES: result})


###
class SumMethod(Component, Executor):
    def execute(self, x: int, y: int) -> int:
        return x + y


class SumAction(Component, components=[SumMethod]):
    pass


if __name__ == "__main__":
    print(SumAction()[Executor].execute(x=1, y=3))
