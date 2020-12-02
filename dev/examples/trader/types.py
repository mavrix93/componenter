import abc
from typing import Generic, TypeVar, Protocol, Optional

DataQueryT = TypeVar("DataQueryT")
MarketDataT = TypeVar("MarketDataT")
TransformedMarketDataT = TypeVar("TransformedMarketDataT")
ActionDecisionT = TypeVar("ActionDecisionT")
ActionResultT = TypeVar("ActionResultT")
PredictionT = TypeVar("PredictionT")


class ReversibleP(Protocol):
    def reverse(self: MarketDataT) -> MarketDataT:
        ...


class AverageableP(Protocol):
    def average(self: MarketDataT) -> float:
        ...


class IndexableP(Protocol):
    def first(self) -> float:
        ...

    def last(self) -> float:
        ...


class NumericScoreP(Protocol):
    value: float
    name: str
    meta: Optional[dict] = None


ReversibleMarketDataT = TypeVar("ReversibleMarketDataT", bound=ReversibleP)
AverageableDataT = TypeVar("AverageableDataT", bound=AverageableP)
NumericScoreT = TypeVar("NumericScoreT", bound=NumericScoreP)
IndexableT = TypeVar("IndexableT", bound=IndexableP)


class ComputableP(AverageableP, ReversibleP, IndexableP):
    pass


class MarketDataProviderT(Generic[DataQueryT, MarketDataT], abc.ABC):
    @abc.abstractmethod
    def get_data(self, query: DataQueryT) -> MarketDataT:
        ...


class ActionDeciderT(Generic[MarketDataT, ActionDecisionT], abc.ABC):
    @abc.abstractmethod
    def decide(self, data: MarketDataT) -> ActionDecisionT:
        ...


class PredictorT(Generic[MarketDataT, PredictionT], abc.ABC):
    @abc.abstractmethod
    def predict(self, data: MarketDataT) -> PredictionT:
        ...


class RiskEvaluatorT(Generic[PredictionT, ActionDecisionT], abc.ABC):
    @abc.abstractmethod
    def evaluate(self, prediction: PredictionT) -> ActionDecisionT:
        ...


class DataTransformerT(Generic[MarketDataT, TransformedMarketDataT], abc.ABC):
    @abc.abstractmethod
    def transform(self, data: MarketDataT) -> TransformedMarketDataT:
        ...


class ActionExecutorT(Generic[ActionDecisionT, ActionResultT], abc.ABC):
    @abc.abstractmethod
    def execute(self, decision: ActionDecisionT) -> ActionResultT:
        ...
