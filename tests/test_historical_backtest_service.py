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

    def __init__(self) -> None:
        self.updated = 0

    def predict(
        self,
        fixture: dict,
    ) -> dict[str, float]:
        return {
            "H": 0.6,
            "D": 0.2,
            "A": 0.2,
        }

    def update(
        self,
        fixture: dict,
    ) -> None:
        self.updated += 1


class FakeRepository:

    def load(
        self,
    ) -> list[dict]:
        return [
            {
                "home_team": "Pafos FC",
                "away_team": "Omonia",
                "actual_result": "H",
            }
        ]


def test_service_runs_complete_backtest():
    repository = FakeRepository()
    predictor = FakePredictor()

    fixtures = repository.load()

    service = HistoricalBacktestService(
        predictor=predictor,
    )

    report = service.run(
        fixtures=fixtures,
    )

    assert isinstance(
        report,
        BacktestReport,
    )

    assert report.total_matches == 1
    assert predictor.updated == 1