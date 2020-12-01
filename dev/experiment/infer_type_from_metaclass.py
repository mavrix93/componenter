from dataclasses import dataclass
from typing import TypeVar, Generic, Sequence, Type, Tuple

ComponentsT = TypeVar("ComponentsT")


class ComponentMeta(type):
    _component_classes: Sequence[Type["Component"]]

    def __new__(mcs, name, bases, class_attributes, components: Sequence[Type["Component"]] = ()):
        return super().__new__(mcs, name, bases, {**class_attributes, "_component_classes": components})

    @classmethod
    def create(mcs: type, name: str, components: Sequence[Type["Component"]]) -> "ComponentMeta":
        return mcs(name, (object,), {}, components=components)


class Component(Generic[ComponentsT], metaclass=ComponentMeta):
    pass


class Comp1(Component):
    pass


@dataclass
class MyComp(Generic[ComponentsT], Component[ComponentsT]):
    components: Tuple[Component[ComponentsT]]

    def get(self) -> ComponentsT:
        ...


x = MyComp(components=(Component[dict](),))
vv = x.get()
