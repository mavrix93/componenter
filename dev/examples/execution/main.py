from asyncio import get_event_loop

from dev.examples.execution.components import (
    SyncExecutor,
    PrintLogger,
    NoParsing,
    ToJsonParsing,
    AsyncExecutor,
    TaskMethodExecutor,
)
from dev.examples.execution.types import ExecutorComponents, TaskMethodComponents, DataT

if __name__ == "__main__":

    def make_sum(data: dict) -> dict:
        return dict(data, z=data["x"] + data["y"])

    async def async_make_sum(data: dict) -> dict:
        return dict(data, z=data["x"] + data["y"])

    result1 = SyncExecutor(components=ExecutorComponents(logger=PrintLogger(), parser=NoParsing())).run(
        task=make_sum, data=[{"x": 1, "y": 3}]
    )

    result2 = AsyncExecutor(
        components=ExecutorComponents(logger=PrintLogger(), parser=ToJsonParsing()), loop=get_event_loop()
    ).run(task=async_make_sum, data=[{"x": 1, "y": 3}, {"x": 14, "y": 43}, {"x": 31, "y": 23}])

    print(result2)

    class SumTaskMethodExecutor(TaskMethodExecutor):
        def task_method(self, data: dict) -> dict:
            return dict(data, z=data["x"] + data["y"])

    result3 = SumTaskMethodExecutor(
        components=TaskMethodComponents(
            executor=SyncExecutor(components=ExecutorComponents(logger=PrintLogger(), parser=NoParsing()))
        )
    ).run(data=[{"x": 144, "y": 443}, {"x": 314, "y": 243}])
    print(result3)
