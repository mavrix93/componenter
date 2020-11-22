from typing import Optional, Type, Generic, TypeVar, NamedTuple, Any

from pydantic import BaseModel

ComponentConfigT = TypeVar("ComponentConfigT", bound="ComponentConfig")
ComponentT = TypeVar("ComponentT", bound="Component")
ComponentsT = TypeVar("ComponentsT", bound="Components")
ComponentOrProtocolT = TypeVar("ComponentOrProtocolT", "Component", Any)


class ComponentConfig(BaseModel):
    pass


class Components(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class Component(Generic[ComponentConfigT, ComponentsT]):
    def __init__(self, components: ComponentsT, config: ComponentConfigT):
        self.config = config
        self.components: ComponentsT = components

    def __getitem__(self, item: Type[ComponentOrProtocolT]) -> ComponentOrProtocolT:
        for component in self.components.dict().values():
            if isinstance(component, item):
                return component
        raise KeyError
