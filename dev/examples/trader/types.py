import abc
from typing import Generic, TypeVar

DataQueryT = TypeVar("DataQueryT")
MarketDataT = TypeVar("MarketDataT")
ActionDecisionT = TypeVar("ActionDecisionT")
ActionResultT = TypeVar("ActionResultT")


class MarketDataProviderT(Generic[DataQueryT, MarketDataT], abc.ABC):
    @abc.abstractmethod
    def get_data(self, query: DataQueryT) -> MarketDataT:
        ...


class ActionDeciderT(Generic[MarketDataT, ActionDecisionT], abc.ABC):
    @abc.abstractmethod
    def decide(self, data: MarketDataT) -> ActionDecisionT:
        ...


class ActionExecutorT(Generic[ActionDecisionT, ActionResultT], abc.ABC):
    @abc.abstractmethod
    def execute(self, decision: ActionDecisionT) -> ActionResultT:
        ...

