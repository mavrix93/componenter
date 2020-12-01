from typing import TypeVar, Tuple, Generic, NamedTuple

T = TypeVar("T")


class BB:
    pass


class CC(BB):
    pass


class DD:
    pass


class A(Generic[T]):
    def __init__(self, value: Tuple[str, T, BB]):
        self.value = value

    def get(self) -> T:
        pass


class InpType(NamedTuple):
    first: str
    second: dict


aa = A(("vvv", {}, CC()))
x = aa.get()
