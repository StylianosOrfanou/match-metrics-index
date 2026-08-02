from validation.backtest_runner import (
    BacktestRunner,
)
from validation.backtest_report import (
    BacktestReport,
)


class FakePredictor:

    def predict(
        self,
        fixture,
    ):
        return {
            "H": 0.60,
            "D": 0.25,
            "A": 0.15,
        }


def test_runner_returns_backtest_report():
    runner = BacktestRunner(
        predictor=FakePredictor(),
    )

    fixtures = [
        {
            "home_team": "Team A",
            "away_team": "Team B",
            "actual_result": "H",
        },
    ]

    report = runner.run(
        fixtures,
    )

    assert isinstance(
        report,
        BacktestReport,
    )

def test_runner_calculates_log_loss():
    runner = BacktestRunner(
        predictor=FakePredictor(),
    )

    report = runner.run(
        [
            {
                "home_team": "Team A",
                "away_team": "Team B",
                "actual_result": "H",
            },
        ]
    )

    assert report.log_loss > 0