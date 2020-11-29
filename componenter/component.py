import abc
from typing import Type, Generic, TypeVar, Any, List, Optional, ClassVar, Tuple, Sequence, Union

from pydantic import BaseModel, validator
from pydantic.main import ModelMetaclass

from componenter.utils import unwrap_type

ComponentT = TypeVar("ComponentT", bound="Component")
ComponentsT = TypeVar("ComponentsT", bound=Sequence)
ComponentOrProtocolT = TypeVar("ComponentOrProtocolT", "Component", Any)


class ComponentMeta(ModelMetaclass):
    _component_classes: ClassVar[Sequence[Type["Component"]]]

    def __new__(mcs, name, bases, class_attributes, components: Sequence[Type["Component"]] = ()):
        return super().__new__(mcs, name, bases, {**class_attributes, "_component_classes": components})

    @classmethod
    def create(mcs: type, name: str, components: Sequence[Type["Component"]]) -> "ComponentMeta":
        return mcs(name, (object,), {}, components=components)


class Component(Generic[ComponentsT], BaseModel, abc.ABC, metaclass=ComponentMeta):
    components: Union[ComponentsT, tuple] = ()

    @validator("components")
    def correct_components(cls, components: ComponentsT):
        n_len = len(cls._component_classes)

        if not n_len == len(components):
            raise ValueError(
                "Number of expected components ({}) doesn't match the provided number of components ({})".format(
                    n_len, len(components)
                )
            )
        for i in range(n_len):
            if not isinstance(components[i], unwrap_type(cls._component_classes[i])):
                raise ValueError(
                    "Component class {} was not found among provided components: {}".format(
                        cls._component_classes[i], components[i]
                    )
                )
        return components

    class Config:
        arbitrary_types_allowed = True

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.update_forward_refs()

    def __getitem__(self, item: Type[ComponentOrProtocolT]) -> ComponentOrProtocolT:
        for component in self.components or []:
            if isinstance(component, item):
                return component
        raise KeyError
