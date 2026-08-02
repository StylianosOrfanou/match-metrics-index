from scripts.run_backtest import (
    run_backtest,
)


class FakeRepository:

    def load(self):
        return [
            {
                "home_team": "Pafos FC",
                "away_team": "Omonia",
                "actual_result": "H",
            }
        ]


class FakePredictor:

    def predict(
        self,
        fixture,
    ):
        return {
            "H": 0.6,
            "D": 0.2,
            "A": 0.2,
        }


def test_run_backtest_returns_report():
    report = run_backtest(
        repository=FakeRepository(),
        predictor=FakePredictor(),
    )

    assert report.total_matches == 1