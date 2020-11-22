from typing import Optional, Type, List, Generic, TypeVar, Dict

ComponentsContainerType = TypeVar("ComponentsContainerType")
SomeComponent = TypeVar("SomeComponent")


class ComponentsClassConfig(Generic[ComponentsContainerType]):
    pass


class Component(Generic[ComponentsContainerType]):
    def __init__(self, parent: ComponentsContainerType):
        self.parent = parent


class ComponentsMeta(type):
    def __new__(mcs, name, bases, class_attributes, components: Optional[List[Type[Component]]] = None):
        cls = super().__new__(mcs, name, bases, class_attributes)
        cls._components_classes: Dict[str, Type[Component]] = getattr(cls, "_components_classes", []) + (
            components or []
        )
        return cls


class ComponentsContainer(metaclass=ComponentsMeta):
    def __init__(self):
        self.components: Dict[
            Type[Component["ComponentsContainer"]], Component[ComponentsContainer]
        ] = self._init_components()

    def __getitem__(self, item: Type[SomeComponent]) -> SomeComponent:
        return self.components[item]

    def _init_components(self) -> Dict[Type[Component["ComponentsContainer"]], Component["ComponentsContainer"]]:
        return {comp: comp(parent=self) for comp in self.__class__._components_classes or []}
