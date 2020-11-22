import abc
from typing import Type, Generic, TypeVar, Any

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


class Component(Generic[ComponentConfigT, ComponentsT], BaseModel, abc.ABC):
    config: ComponentConfigT
    components: ComponentsT

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.update_forward_refs()

    def __getitem__(self, item: Type[ComponentOrProtocolT]) -> ComponentOrProtocolT:
        for component in self.components.__dict__.values():
            if isinstance(component, item):
                return component
        raise KeyError
