from typing import TypeVar, Generic, List, Type, runtime_checkable

from typeguard import check_type

T1 = TypeVar("T1")
T2 = TypeVar("T2")


class A(Generic[T1]):
    pass


# def match(options: List[Type], searched):
#     for op in options:
#         print(isinstance(searched, op))
#
#
# if __name__ == "__main__":
#     match([A[int], A[str]], A[int])

if __name__ == "__main__":
    check_type("bla", A(), A[int])
