from dev.examples.actions.components import NoChangeRunner, MethodExecutor, ValidationExecutor, ExecutionChain
from dev.examples.actions.configs import (
    RunnerComponents,
    MethodExecutorConfig,
    MethodValidationExecutorConfig,
    ExecutionChainComponents,
)
from dev.examples.actions.types import DataContainer, IExecutor

if __name__ == "__main__":
    runner = NoChangeRunner(
        components=RunnerComponents(
            executor=MethodExecutor(
                config=MethodExecutorConfig(method=lambda name, age: print("Name", name, "age", age))
            )
        )
    )

    validator = NoChangeRunner(
        components=RunnerComponents(
            executor=ValidationExecutor(config=MethodValidationExecutorConfig(method=lambda name, age: age > 18))
        )
    )

    class Person(DataContainer):
        name: str
        age: int

    runner.run(Person(name="johan", age=39))

    validator.run(Person(name="johan", age=19))

    runner[IExecutor].execute(name="GG", age=1)

    ExecutionChain(components=ExecutionChainComponents(runners=[runner, validator])).run_chain(
        Person(name="johan", age=39)
    )
