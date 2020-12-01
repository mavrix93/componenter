from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")


@dataclass
class Component(Generic[T]):
    components: T = None


@dataclass
class Impl(Component[str]):
    xx: int


if __name__ == "__main__":
    im = Impl(components="dfd", xx=10)
    print(im.components, im.xx)
