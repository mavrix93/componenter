from typing import Protocol, Union, _SpecialForm


class IAttacker(Protocol):
    def attack(self):
        pass


class IDefender(Protocol):
    def defend(self):
        pass


And: _SpecialForm = _SpecialForm("And")


class Attacker:
    def attack(self):
        pass


class Defender:
    def defend(self):
        pass


Ad = type("...", (Attacker, Defender), {})


class Battle:
    def __init__(self, warrior: Ad):
        warrior.attack()
        warrior.defend()
