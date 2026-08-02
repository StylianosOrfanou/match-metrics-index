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

from validation.historical_fixture_repository import (
    HistoricalFixtureRepository,
)


def test_runner_accepts_repository(tmp_path):
    filepath = (
        tmp_path
        / "fixtures.json"
    )

    filepath.write_text(
        """
[
    {
        "home_team":"A",
        "away_team":"B",
        "actual_result":"H"
    }
]
""",
        encoding="utf-8",
    )

    repository = (
        HistoricalFixtureRepository(
            filepath=str(filepath),
        )
    )

    runner = BacktestRunner(
        predictor=FakePredictor(),
    )

    report = runner.run(
        repository.load(),
    )

    assert report.total_matches == 1