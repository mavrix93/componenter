from typing import TypedDict


class CatInput(TypedDict):
    name: str
    age: int


class Cat:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def create(cls, inp: CatInput):
        return cls(**inp)
