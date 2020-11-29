from typing import TypeVar, Tuple, Generic, NamedTuple

T = TypeVar("T")


class A(Generic[T]):
    def __init__(self, value: Tuple[str, T]):
        self.value = value

    def get(self) -> T:
        pass


class InpType(NamedTuple):
    first: str
    second: dict


aa = A(("vvv", {}))
x = aa.get()
