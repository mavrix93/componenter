from typing import Optional, Type, Generic, TypeVar, runtime_checkable, Protocol, NamedTuple, Any

ComponentConfigT = TypeVar("ComponentConfigT", bound=Optional[tuple])
ComponentT = TypeVar("ComponentT", bound="Component")
ComponentsT = TypeVar("ComponentsT", bound=Optional[tuple])
T = TypeVar("T")
ComponentOrProtocolT = TypeVar("ComponentOrProtocolT", "Component", Any)


class ComponentConfig(NamedTuple):
    pass


class Component(Generic[ComponentConfigT, ComponentsT]):
    def __init__(self, components: ComponentsT = None, config: ComponentConfigT = None):
        self.config = config
        self.components: ComponentsT = components or tuple()

    def __getitem__(self, item: Type[ComponentOrProtocolT]) -> ComponentOrProtocolT:
        for component in self.components:
            # if issubclass(component.__class__, item):
            #     return component
            if isinstance(component, item):
                return component
        raise KeyError


##


class Heart(Component):
    def get_heart_rate(self) -> int:
        return 60


class HumanHeart(Heart):
    def get_heart_rate(self) -> int:
        return 120


class BrainConfig(NamedTuple):
    iq: int


class Brain(Component[BrainConfig, None]):
    def calculate_iq(self):
        return self.config.iq


class ChickenBrain(Brain):
    pass


class HeadComponents(NamedTuple):
    brain: Brain


class Head(Component[None, HeadComponents]):
    def get_iq(self):
        return self[Brain].calculate_iq()


class HumanComponents(NamedTuple):
    head: Head
    heart: Heart


class Human(Component[None, HumanComponents]):
    pass


@runtime_checkable
class WithHeartRate(Protocol):
    def get_heart_rate(self) -> int:
        ...


if __name__ == "__main__":
    human = Human(
        components=HumanComponents(
            head=Head(components=HeadComponents(brain=ChickenBrain(config=BrainConfig(iq=123)))), heart=Heart()
        )
    )
    print(human[Head][Brain].calculate_iq())
    print(human[WithHeartRate].get_heart_rate())
