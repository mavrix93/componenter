from typing import Protocol, Generic, TypeVar


class BaseRunner(Protocol):
    def run(self):
        pass


T = TypeVar("T")


class A(Generic[T]):
    a: T


x = A[int]().a
x
