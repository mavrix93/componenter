from dataclasses import dataclass
from typing import TypedDict, List, Tuple, Generic

from componenter.component import Component
from dev.examples.trader.types import (
    MarketDataProviderT,
    DataQueryT,
    MarketDataT,
    ActionDeciderT,
    ActionExecutorT,
    ActionDecisionT,
    ActionResultT,
)


@dataclass
class MarketDataQuery:
    market: str


class DummyMarketData(TypedDict):
    time: int
    value: int


class DummyMarketDataProvider(MarketDataProviderT[MarketDataQuery, List[DummyMarketData]]):
    def get_data(self, query: MarketDataQuery) -> List[DummyMarketData]:
        return [{"time": 1, "value": 2}, {"time": 2, "value": 4}, {"time": 3, "value": 9}]


class AlwaysBuyDecider(Generic[MarketDataT], ActionDeciderT[MarketDataT, bool]):
    def decide(self, data: MarketDataT) -> bool:
        return True


class NothingToExecute(ActionExecutorT[bool, str]):
    def execute(self, decision: bool) -> str:
        return "Executing: {}".format(decision)


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
