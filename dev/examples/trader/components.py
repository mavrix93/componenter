from dataclasses import dataclass
from enum import Enum, auto
from typing import TypedDict, List, Tuple, Generic, TypeVar, Optional

from componenter.component import Component
from dev.examples.trader.types import (
    MarketDataProviderT,
    DataQueryT,
    MarketDataT,
    ActionDeciderT,
    ActionExecutorT,
    ActionDecisionT,
    ActionResultT,
    PredictorT,
    RiskEvaluatorT,
    DataTransformerT,
    ReversibleMarketDataT,
    NumericScoreT,
    ReversibleP,
    PredictionT,
    AverageableDataT,
    AverageableP,
    NumericScoreP,
    IndexableP,
    ComputableP,
)


# --- General
class Broker(
    Generic[DataQueryT, MarketDataT, ActionDecisionT, ActionResultT],
    Component[
        Tuple[
            MarketDataProviderT[DataQueryT, MarketDataT],
            ActionDeciderT[MarketDataT, ActionDecisionT],
            ActionExecutorT[ActionDecisionT, ActionResultT],
        ],
    ],
):
    def think_and_act(self, market: str) -> ActionResultT:
        return self[ActionExecutorT].execute(
            self[ActionDeciderT].decide(self[MarketDataProviderT].get_data(MarketDataQuery(market=market)))
        )


class EvaluatePredictionDecider(
    Generic[MarketDataT, PredictionT, ActionDecisionT],
    Component[Tuple[PredictorT[MarketDataT, PredictionT], RiskEvaluatorT[PredictorT, ActionDecisionT]]],
    ActionDeciderT[MarketDataT, ActionDecisionT],
):
    def decide(self, data: MarketDataT) -> ActionDecisionT:
        return self[RiskEvaluatorT].evaluate(self[PredictorT].predict(data))


class MeanGradientTransformer(DataTransformerT[ComputableP, "SimpleNumericScore"]):
    def transform(self, data: ComputableP) -> "SimpleNumericScore":
        return SimpleNumericScore(name="mean-gradient", value=data.last() / data.average())


# --- Dummy general


class ReverseTransformer(
    Generic[ReversibleMarketDataT], DataTransformerT[ReversibleMarketDataT, ReversibleMarketDataT]
):
    def transform(self, data: ReversibleMarketDataT) -> ReversibleMarketDataT:
        return data.reverse()


class ReverseHistoryPredictor(
    Generic[ReversibleMarketDataT, NumericScoreT],
    PredictorT[ReversibleMarketDataT, NumericScoreT],
    Component[Tuple[ReverseTransformer[ReversibleMarketDataT], DataTransformerT[ReversibleMarketDataT, NumericScoreT]]],
):
    def predict(self, data: ReversibleMarketDataT) -> NumericScoreT:
        return self.components[1].transform(self.components[0].transform(data))


class ThresholdEvaluator(RiskEvaluatorT[NumericScoreT, "SimpleOrder"]):
    # TODO
    THRESHOLD = 0.5
    BASE_AMOUNT = 100

    def evaluate(self, prediction: NumericScoreT) -> "SimpleOrder":
        ratio = prediction.value / self.THRESHOLD
        if ratio > 1:
            return SimpleOrder(amount=int(ratio * self.BASE_AMOUNT), action=OrderAction.BUY)
        return SimpleOrder(action=OrderAction.DO_NOTHING)


# --- Implementations


@dataclass
class MarketDataQuery:
    market: str


class ValueTimeDataPoint(TypedDict):
    time: int
    value: int


@dataclass
class SimpleNumericScore:
    value: float
    name: str
    meta: Optional[dict] = None


class ValueTimeData(ReversibleP, AverageableP, IndexableP):
    def __init__(self, *data: ValueTimeDataPoint):
        self._data = data

    def reverse(self) -> "ValueTimeData":
        n_len = len(self._data)
        times = [d["time"] for d in self._data]
        values = [d["value"] for d in self._data]
        return ValueTimeData(*[ValueTimeDataPoint(time=times[i], value=values[n_len - i]) for i in range(n_len)])

    def average(self) -> float:
        return sum(d["value"] for d in self._data) / len(self._data)

    def first(self) -> float:
        return self._data[0]["value"]

    def last(self) -> float:
        return self._data[-1]["value"]


class OrderAction(Enum):
    BUY = auto()
    SELL = auto()
    DO_NOTHING = auto()


@dataclass
class SimpleOrder:
    action: OrderAction
    amount: float = 0


class DummyMarketDataProvider(MarketDataProviderT[MarketDataQuery, ValueTimeData]):
    def get_data(self, query: MarketDataQuery) -> ValueTimeData:
        return ValueTimeData({"time": 1, "value": 2}, {"time": 2, "value": 4}, {"time": 3, "value": 9})


class AlwaysBuyDecider(Generic[MarketDataT], ActionDeciderT[MarketDataT, bool]):
    def decide(self, data: MarketDataT) -> bool:
        return True


class NothingToExecute(ActionExecutorT[bool, str]):
    def execute(self, decision: bool) -> str:
        return "Executing: {}".format(decision)
