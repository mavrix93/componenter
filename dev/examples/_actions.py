from dev.version1 import Component, ComponentsContainer, ComponentsContainerType


class Executor(Component[ComponentsContainerType]):
    def run(self):
        pass


class MethodExecutor(Executor[ComponentsContainerType]):
    def __init__(self, parent):
        super().__init__(parent=parent)

    def run(self, *args, **kwargs):
        # TODO..
        return self.parent[ExecutionMethod]


class ValidationExecutor(Executor):
    def run(self, *args, **kwargs):
        if not self.parent[Validator].validate(*args, **kwargs):
            raise ValueError("Failed to validate")


class Validator(Component):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.validate_method = self.parent.validate_method

    def validate(self, *args, **kwargs) -> bool:
        return self.validate_method(*args, **kwargs)


###


class ExecutionMethod(Component[ComponentsContainerType]):
    @staticmethod
    def run_method(x: int, y: int) -> int:
        pass


class SumMethod(ExecutionMethod[ComponentsContainerType]):
    @staticmethod
    def run_method(x: int, y: int) -> int:
        return x + y


class Action(ComponentsContainer, components=[MethodExecutor, SumMethod]):
    action_meta = None


class Condition(ComponentsContainer, components=[ValidationExecutor, Validator]):
    @staticmethod
    def validate_method(x: int):
        return x > 0


##

if __name__ == "__main__":
    action = Action()
    ll = MethodExecutor(action).parent
    print(action[MethodExecutor].run(10, 13))

    condition = Condition()
    print(condition[ValidationExecutor].run(-1))
