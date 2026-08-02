from validation.backtest_report import (
    BacktestReport,
)
from validation.historical_backtest_service import (
    HistoricalBacktestService,
)
from validation.time_aware_predictor import (
    TimeAwarePredictor,
)


class FakePredictor(
    TimeAwarePredictor,
):

    def __init__(self):
        self.updated = 0

    def predict(
        self,
        fixture,
    ):
        return {
            "H": 0.60,
            "D": 0.25,
            "A": 0.15,
        }

    def update(
        self,
        fixture,
    ):
        self.updated += 1


def test_service_runs_backtest():
    predictor = FakePredictor()

    service = HistoricalBacktestService(
        predictor,
    )

    report = service.run(
        fixtures=[
            {
                "actual_result": "H",
            },
            {
                "actual_result": "A",
            },
        ]
    )

    assert isinstance(
        report,
        BacktestReport,
    )

    assert predictor.updated == 2