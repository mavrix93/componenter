from typing import Protocol


class IAttacker(Protocol):
    def attack(self):
        pass


class IDefender(Protocol):
    def defend(self):
        pass


class Archer:
    def attack(self):
        print("attack")


class Battle:
    def __init__(self, attacker: IAttacker):
        self.attacker = attacker

        attacker.attack()
        # attacker.defend()


if __name__ == "__main__":
    x = Battle(Archer())
