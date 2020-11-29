from typing import Literal


class G:
    pass


def bla(x: Literal[G, "bb"]):
    return x


x = bla(1)
