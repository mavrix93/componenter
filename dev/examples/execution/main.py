from typing import Protocol, runtime_checkable

from dev.examples.execution.components import (
    SyncExecutor,
    PrintLogger,
    NoParsing,
    ToJsonParsing,
    AsyncExecutor,
    TaskMethodExecutor,
    EventLoopProvider,
)

if __name__ == "__main__":

    def make_sum(data: dict) -> dict:
        return dict(data, z=data["x"] + data["y"])

    async def async_make_sum(data: dict) -> dict:
        return dict(data, z=data["x"] + data["y"])

    sync_executor = SyncExecutor[dict, dict](components=(PrintLogger(), NoParsing()))
    result1 = sync_executor.run(task=make_sum, data=[{"x": 1, "y": 3}])

    @runtime_checkable
    class LogLike(Protocol):
        def log(self):
            pass

    print(sync_executor[LogLike])

    result2 = AsyncExecutor[dict, str](components=(PrintLogger(), ToJsonParsing(), EventLoopProvider())).run(
        task=async_make_sum, data=[{"x": 1, "y": 3}, {"x": 14, "y": 43}, {"x": 31, "y": 23}]
    )

    class SumTaskMethodExecutor(
        TaskMethodExecutor[dict, dict],
    ):
        def task_method(self, data: dict) -> dict:
            return dict(data, z=data["x"] + data["y"])

    result3 = SumTaskMethodExecutor(components=(SyncExecutor(components=(PrintLogger(), NoParsing())),)).run(
        data=[{"x": 144, "y": 443}, {"x": 314, "y": 243}]
    )
