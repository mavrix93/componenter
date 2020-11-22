from typing import TypedDict, TypeVar, Generic, Type

ConfigType = TypeVar("ConfigType", bound="Config")


class Config(Generic[ConfigType]):
    config_name: str


class BrainConfig(Config):
    brain_id: str


class Component(Generic[ConfigType]):
    CONFIG: Type[ConfigType]

    def __init__(self, config: ConfigType):
        self.config = config


class Brain(Component[BrainConfig]):
    CONFIG = BrainConfig

    def bla(self):
        self.config


if __name__ == "__main__":
    Brain(config=BrainConfig())
