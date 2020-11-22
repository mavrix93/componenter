from typing import List, TypedDict, NamedTuple, Generic, TypeVar


class Comp:
    pass


class CompType1(Comp):
    pass


class CompType2(Comp):
    pass


ComponentsT = TypeVar("ComponentsT")
ConfigT = TypeVar("ConfigT")


class Base(Generic[ComponentsT, ConfigT]):
    Config: ConfigT
    Components: ComponentsT

    def __init__(self, components: ComponentsT, config: ConfigT):
        self.components = components
        self.config = config


Config = NamedTuple("Config", [("name", str), ("age", int)])
Components = NamedTuple("Components", [("comp1", CompType1), ("comp2", CompType2)])


class A(
    Base[Components, Config],
):
    pass


if __name__ == "__main__":
    a = A(components=1, config=1)
    a = A(components=Components(comp1=CompType1(), comp2=CompType2()), config=Config(name="bla", age=1))
    print(a.config.name, a.components)
