from typing import Type

from returns.context import RequiresContext


class Component1:
    def __init__(self, components, x, y):
        pass

    @staticmethod
    def create(x, y) -> RequiresContext["Component1", tuple]:
        return RequiresContext(lambda components: Component1(components, x, y))

    def ping(self) -> "Component1":
        print("---", self)
        return self


class Component2:
    def __init__(self, x, y):
        pass

    def __class_getitem__(cls, components) -> Type["Component2"]:
        return cls


if __name__ == "__main__":
    ff = Component1.create(1, 2)
    print(ff.map(lambda inp: inp.ping())([9, 9]))
