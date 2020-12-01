import abc
from typing import Type, Generic, TypeVar, Any, Optional, Sequence, final

ComponentT = TypeVar("ComponentT", bound="Component")
ComponentsT = TypeVar("ComponentsT", bound=Optional[Sequence])
ComponentOrProtocolT = TypeVar("ComponentOrProtocolT", "Component", Any)


class Component(Generic[ComponentsT], abc.ABC):
    def __init__(self, components: ComponentsT):
        self.components = components

    def __getitem__(self, item: Type[ComponentOrProtocolT]) -> ComponentOrProtocolT:
        for component in self.components or []:
            if isinstance(component, item):
                return component
        raise KeyError(item)


class ComponentWithoutComponents(Component[None]):
    def __init__(self):
        super().__init__(components=None)
