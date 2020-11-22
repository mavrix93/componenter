from typing import Optional, Type, Generic, TypeVar, NamedTuple, Any

ComponentConfigT = TypeVar("ComponentConfigT", bound=Optional[tuple])
ComponentT = TypeVar("ComponentT", bound="Component")
ComponentsT = TypeVar("ComponentsT", bound=Optional[tuple])
ComponentOrProtocolT = TypeVar("ComponentOrProtocolT", "Component", Any)


class ComponentConfig(NamedTuple):
    pass


class Component(Generic[ComponentConfigT, ComponentsT]):
    def __init__(self, components: ComponentsT = None, config: ComponentConfigT = None):
        self.config = config
        self.components: ComponentsT = components or tuple()

    def __getitem__(self, item: Type[ComponentOrProtocolT]) -> ComponentOrProtocolT:
        for component in self.components:
            if isinstance(component, item):
                return component
        raise KeyError
