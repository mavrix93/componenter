from typing import List

from dev.examples.trader.components import (
    Broker,
    DummyMarketDataProvider,
    AlwaysBuyDecider,
    NothingToExecute,
    DummyMarketData,
    MarketDataQuery,
)

# IDEA: Use set instead of tuple. Can it be type checked?
if __name__ == "__main__":
    broker = Broker[MarketDataQuery, List[DummyMarketData], bool, str](
        components=(DummyMarketDataProvider(), AlwaysBuyDecider(), NothingToExecute())
    )
    result = broker.think_and_act(market="some-marker")
    print(result)
