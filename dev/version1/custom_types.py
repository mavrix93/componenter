from typing import Union, _SpecialForm

# class MyUnion(Union.__class__):
# def __getitem__(self, parameters):
#     # raise ValueError("--")
#     if parameters == ():
#         raise TypeError("Cannot take a Union of no types.")
#     if not isinstance(parameters, tuple):
#         parameters = (parameters,)
#     if self.__origin__ is None:
#         msg = "Union[arg, ...]: each arg must be a type."
#     else:
#         msg = "Parameters to generic types must be types."
#     # parameters = tuple(_type_check(p, msg) for p in parameters)
#
#     return self.__class__(parameters, origin=self, _root=True)
#  pass

MyUnion = _SpecialForm("Union", "docs")


def bla(x: MyUnion[str, float]):
    return x


if __name__ == "__main__":
    y = bla(10)


