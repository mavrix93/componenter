from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1, SupportsKind2, Kind2

BuildingT = TypeVar("BuildingT")
MaterialT = TypeVar("MaterialT")
_ProcedureT = TypeVar("_ProcedureT", bound="ProcedureT")


class ProcedureT(Generic[BuildingT, MaterialT]):
    def process(self, material: MaterialT) -> BuildingT:
        ...


class Procedure(Kind2["Procedure", BuildingT, MaterialT], ProcedureT[BuildingT, MaterialT]):
    def process(self, material: MaterialT) -> BuildingT:
        ...


class InverseProcedure(Kind2["Procedure", BuildingT, MaterialT], ProcedureT[MaterialT, BuildingT]):
    def process(self, material: BuildingT) -> MaterialT:
        ...


class Builder(Kind2["Builder", BuildingT, MaterialT]):
    def __init__(self, procedure: ProcedureT[BuildingT, MaterialT], material: MaterialT):
        ...

    def build(self) -> BuildingT:
        ...


class Company(
    Generic[BuildingT, MaterialT],
):
    def __init__(self, builder: Builder[BuildingT, MaterialT]):
        pass

    def get_building(self) -> BuildingT:
        ...


xbuilder = Builder(procedure=Procedure[str, int](), material=11)
yy = xbuilder.build()


def invert(inst: Kind2[_ProcedureT, BuildingT, MaterialT]) -> Kind2[_ProcedureT, MaterialT, BuildingT]:
    ...


z = invert(Procedure[str, int]())
ff = Procedure[str, int]().process(111)
