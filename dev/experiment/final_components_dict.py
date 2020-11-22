from typing import List, Optional, Type, TypedDict, Tuple, TypeVar


class Organ:
    pass


class Brain(Organ):
    brain_id: str


class Heart(Organ):
    pass


T1 = TypeVar("T1")
T2 = TypeVar("T2")


class Meta(type):
    def __new__(mcs, name, bases, class_attributes, organs: Optional[Tuple[Type[T1], Type[T2]]] = None):
        cls = super().__new__(mcs, name, bases, class_attributes)

        # class OrgansType(TypedDict):
        #     Brain: Brain
        #     Heart: Heart

        OrgansType = TypedDict("OrgansType", {"T1": T1, "T2": T2})

        cls.organs: OrgansType = {organ_cls: organ_cls() for organ_cls in (organs or [])}

        # x = cls.organs["Brainx"]
        return cls


class Body(metaclass=Meta, organs=[Brain]):
    pass


ff = Body().organs["T1"]
