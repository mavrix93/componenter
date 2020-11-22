from dataclasses import dataclass


class Heart:
    pass


@dataclass
class BrainConfig:
    iq: int


class Brain(config=BrainConfig):
    def __init__(self, config: BrainConfig):
        self.iq = config.iq

    def calculate_iq(self):
        return self.iq


class Head(componenets=[Brain]):
    def get_iq(self):
        self[Brain].calculate_iq()


class Human(components=[Heart, Head]):
    pass
