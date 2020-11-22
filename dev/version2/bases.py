from dataclasses import dataclass
from typing import Optional, Type, List, Generic
from dev.version2.types import ComponentT, ComponentGenConfigT, ComponentConfigT, ComponentGenT


class ComponentsMeta(type):
    def __init__(
        cls,
        *args,
        components: Optional[List[Type["ComponentT"]]] = None,
        config: Optional[Type[ComponentConfigT]] = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        cls.COMPONENTS_CLASSES: List[Type[ComponentT]] = components or []
        cls.CONFIG: Optional[Type[ComponentConfigT]] = config

    def __new__(
        mcs,
        name,
        bases,
        class_attributes,
        components: Optional[List[Type["ComponentT"]]] = None,
        config=Type[ComponentConfigT],
    ):
        return super().__new__(mcs, name, bases, class_attributes)

    # def __new__(
    #     mcs,
    #     name,
    #     bases: Tuple[Type[ComponentT]],
    #     class_attributes,
    #     components: Optional[List[Type[ComponentT]]] = None,
    #     config: Optional[Type[ComponentConfigT]] = None,
    # ):
    #     cls: Type[ComponentT] = super().__new__(mcs, name, bases, class_attributes)
    #
    #     cls.COMPONENTS_CLASSES = components or []
    #     cls.CONFIG = config
    #     return cls


class Component(Generic[ComponentGenConfigT], metaclass=ComponentsMeta):
    COMPONENTS_CLASSES: List[Type["ComponentT"]]
    CONFIG: Optional[Type[ComponentGenConfigT]]

    config: ComponentGenConfigT

    def __init__(self, configs: List[ComponentConfigT] = None):
        self.config = self._get_config(configs=configs or [])
        self.components = {
            component_cls: component_cls(configs=configs or []) for component_cls in self.COMPONENTS_CLASSES
        }

        # TODO
        super().__init__(configs=configs or [])

    def __getitem__(self, item: Type[ComponentGenT]) -> "ComponentGenT":
        found = self._get_exact(item) or self._find_of_type(item)

        if not found:
            raise KeyError("Not found: {}".format(item))
        return found

    def _get_exact(self, item: Type[ComponentGenT]) -> Optional["ComponentGenT"]:
        return self.components.get(item)

    def _find_of_type(self, item: Type[ComponentGenT]) -> Optional["ComponentGenT"]:
        for component_cls, component in self.components.items():
            if issubclass(component_cls, item):
                return component

    @classmethod
    def _get_config(cls, configs: List[ComponentConfigT]) -> Optional[ComponentConfigT]:
        if cls.CONFIG:
            for config in configs:
                if isinstance(config, cls.CONFIG):
                    return config
        return None


##
class Heart(Component):
    pass


@dataclass
class BrainConfig(ComponentConfigT):
    iq: int


class NoConfig(ComponentConfigT):
    pass


class Brain(Component[BrainConfig], config=BrainConfig):
    def calculate_iq(self):
        return self.config.iqq


class Head(Component, components=[Brain]):
    def get_iq(self):
        return self[Brain].calculate_iq()


class Human(Component, components=[Heart, Head]):
    pass


if __name__ == "__main__":
    human = Human(configs=[BrainConfig(iq=1)])
    print(human[Head][Brain].calculate_iq())
    print(human[Head][Brain])
