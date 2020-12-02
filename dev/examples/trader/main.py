from typing import List

from componenter.component import Component
from dev.examples.trader.components import (
    Broker,
    DummyMarketDataProvider,
    AlwaysBuyDecider,
    NothingToExecute,
    MarketDataQuery,
    ValueTimeData,
    EvaluatePredictionDecider,
    ReverseHistoryPredictor,
    ThresholdEvaluator,
    ReverseTransformer,
    MeanGradientTransformer,
    SimpleNumericScore,
)

# IDEA: Use set instead of tuple. Can it be type checked?
if __name__ == "__main__":
    print(
        "dummy",
        Broker[MarketDataQuery, ValueTimeData, bool, str](
            components=(DummyMarketDataProvider(), AlwaysBuyDecider(), NothingToExecute())
        ).think_and_act(market="some-marker"),
    )

    ReverseHistoryPredictor[ValueTimeData, SimpleNumericScore](
        components=(ReverseTransformer(), MeanGradientTransformer())
    )

    print(
        "reverse mean",
        Broker[MarketDataQuery, ValueTimeData, bool, str](
            components=(
                DummyMarketDataProvider(),
                EvaluatePredictionDecider(
                    components=(
                        ReverseHistoryPredictor(components=(ReverseTransformer(), MeanGradientTransformer())),
                        ThresholdEvaluator(),
                    )
                ),
                NothingToExecute(),
            )
        ),
    )
