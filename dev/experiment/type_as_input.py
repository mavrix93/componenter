from typing import TypedDict, TypeVar, Generic, Type

ConfigType = TypeVar("ConfigType")


class Config(Generic[ConfigType]):
    config_name: str


class BrainConfig(Config):
    brain_id: str


class Component(Generic[ConfigType]):
    def __init__(self, config: ConfigType):
        self.config = config


class Brain(Component[BrainConfig]):
    def bla(self):
        self.config.brain_id


if __name__ == "__main__":
    Brain(config=BrainConfig())
