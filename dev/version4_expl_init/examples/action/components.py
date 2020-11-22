from typing import Any, Dict, Type, Generic
from dev.version4_expl_init.bases import Component
from dev.version4_expl_init.examples.action.types import ExecutorT, DataContainerT, RunnerT


class Container(DataContainerT):
    def __init__(self, **kwargs):
        self.data = kwargs

    @classmethod
    def from_dict(cls, params: Dict[str, Any]) -> "DataContainerT":
        return cls(**params)

    def to_dict(self) -> Dict[str, Any]:
        return self.data


class ExecutorRunner(RunnerT):
    DATA_CONTAINER: Type[DataContainerT]
    PROVIDES: str

    def run(self, data: DataContainerT) -> DataContainerT:
        return self.wrap(self[ExecutorT].execute(**self.unwrap(data)))

    def unwrap(self, data: DataContainerT) -> Dict[str, Any]:
        return data.to_dict()

    def wrap(self, result: Any) -> DataContainerT:
        return self.DATA_CONTAINER.from_dict({self.PROVIDES: result})


###
class SumMethod(ExecutorT):
    def execute(self, x: int, y: int) -> int:
        return x + y




if __name__ == "__main__":
    print(ExecutorRunner(components=[]))
