from dataclasses import dataclass
from typing import Optional, Type, List, Generic
from dev.version3_no_meta import ComponentT, ComponentGenConfigT, ComponentConfigT, ComponentGenT


class Component(ComponentT[ComponentGenConfigT], Generic[ComponentGenConfigT]):
    COMPONENTS_CLASSES: List[Type["ComponentT"]]
    CONFIG: Optional[Type[ComponentGenConfigT]]

    bla: ComponentGenConfigT

    def __init__(self, configs: List[ComponentConfigT] = None):
        self.config = self._get_config(configs=configs or [])
        self.components = {
            component_cls: component_cls(configs=configs or []) for component_cls in self.COMPONENTS_CLASSES
        }

    def __init_subclass__(
        cls,
        components: Optional[List[Type["ComponentT"]]] = None,
        config: Optional[Type[ComponentConfigT]] = None,
    ):
        cls.COMPONENTS_CLASSES: List[Type[ComponentT]] = components or []
        cls.CONFIG: Optional[Type[ComponentConfigT]] = config
        super().__init_subclass__()

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
    def _get_config(cls, configs: List[ComponentConfigT]) -> Optional[ComponentGenConfigT]:
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
        return self.config.iq


class Head(Component, components=[Brain]):
    def get_iq(self):
        return self[Brain].calculate_iq()


class Human(Component, components=[Heart, Head]):
    pass


if __name__ == "__main__":
    human = Human(configs=[BrainConfig(iq=1)])
    print(human[Head][Brain].calculate_iq())
    print(human[Head][Brain])
