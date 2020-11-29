import abc
from typing import Type, Generic, TypeVar, Any, List, Optional, ClassVar, Tuple

from pydantic import BaseModel, validator
from pydantic.main import ModelMetaclass

ComponentConfigT = TypeVar("ComponentConfigT", bound="ComponentConfig")
ComponentT = TypeVar("ComponentT", bound="Component")
ComponentsT = TypeVar("ComponentsT", bound="Components")
ComponentOrProtocolT = TypeVar("ComponentOrProtocolT", "Component", Any)


class ComponentConfig(BaseModel):
    pass


class ComponentMeta(ModelMetaclass):
    _component_classes: ClassVar[Tuple[Type["Component"]]]

    def __new__(mcs, name, bases, class_attributes, components: Optional[Tuple[Type["Component"]]] = None):
        return super().__new__(mcs, name, bases, {**class_attributes, "_component_classes": components or []})

    @classmethod
    def create(mcs: type, name: str, components: Tuple[Type["Component"]]) -> "ComponentMeta":
        return mcs(name, (object,), {}, components=components)


class Components(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class Component(Generic[ComponentConfigT, ComponentsT], BaseModel, abc.ABC, metaclass=ComponentMeta):
    config: Optional[ComponentConfigT] = None
    components: Optional[ComponentsT] = None

    # @validator("components")
    # def valid_components(cls, component_config: Components):
    #     components = component_config.__dict__.values()
    #
    #     for component_cls in cls._component_classes:
    #         if not (any(isinstance(component, component_cls) for component in components)):
    #             raise ValueError(
    #                 "Component class {} was not found among provided components: {}".format(component_cls, components)
    #             )
    #     return component_config

    class Config:
        arbitrary_types_allowed = True

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.update_forward_refs()

    def __getitem__(self, item: Type[ComponentOrProtocolT]) -> ComponentOrProtocolT:
        for component in self.components.__dict__.values():
            if isinstance(component, item):
                return component
        raise KeyError
