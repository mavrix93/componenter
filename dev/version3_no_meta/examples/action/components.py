from typing import Any, Dict, Type, Generic
from dev.version3_no_meta.bases import Component
from dev.version3_no_meta.examples import ExecutorT, DataContainerT, RunnerT

from dev.version3_no_meta import ComponentGenT


class Container(DataContainerT):
    def __init__(self, **kwargs):
        self.data = kwargs

    @classmethod
    def from_dict(cls, params: Dict[str, Any]) -> "DataContainerT":
        return cls(**params)

    def to_dict(self) -> Dict[str, Any]:
        return self.data


class ExecutorRunner(Generic[ComponentGenT], Component, RunnerT, components=[ExecutorT[ComponentGenT]]):
    DATA_CONTAINER: Type[DataContainerT]
    PROVIDES: str

    def run(self, data: DataContainerT) -> DataContainerT:
        return self.wrap(self[ExecutorT].execute(**self.unwrap(data)))

    def unwrap(self, data: DataContainerT) -> Dict[str, Any]:
        return data.to_dict()

    def wrap(self, result: Any) -> DataContainerT:
        return self.DATA_CONTAINER.from_dict({self.PROVIDES: result})


###
class SumMethod(Component, ExecutorT):
    def execute(self, x: int, y: int) -> int:
        return x + y


class SumAction(Component, components=[SumMethod]):
    pass


if __name__ == "__main__":
    print(SumAction()[ExecutorT].execute(x=1, y=3))
    print(SumAction()[RunnerT].run(Container(x=1, y=3)))
