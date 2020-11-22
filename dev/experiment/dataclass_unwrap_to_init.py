from dataclasses import dataclass
from typing import TypeVar, Generic, TypedDict, Type, NewType

from pydantic import BaseModel


# class Input(TypedDict):
#     x: int
#     y: int


# class Input(BaseModel):
#     x: int
#     y: int


@dataclass
class Input:
    xx: int
    y: int
    z: int


T = TypeVar("T")
TT = NewType("TT", Type[T])


class Creator(Generic[T]):
    def __init__(self, params: Type[T]):
        pass

    def __call__(self, **kwargs):
        print(kwargs, T, TT)
        return TT(**kwargs)


class A:
    create = Creator(Input)

    def __init__(self, **inp: Input):
        pass


if __name__ == "__main__":
    print(A.create(x=1))
