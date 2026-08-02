from engines.prediction_engine import (
    PredictionEngine,
)

from validation.backtest_runner import (
    BacktestRunner,
)
from validation.historical_fixture_repository import (
    HistoricalFixtureRepository,
)
from validation.historical_mmi_predictor import HistoricalMMIPredictor
from validation.mmi_time_aware_predictor import (
    MMITimeAwarePredictor,
)
from engines.historical_rating_builder import (
    HistoricalRatingBuilder,
)
from models.league import League
from repositories.historical_team_state_repository import (
    HistoricalTeamStateRepository,
)
from validation.historical_mmi_predictor import (
    HistoricalMMIPredictor,
)


def run_backtest(
    repository,
    predictor,
):
    fixtures = repository.load()

    runner = BacktestRunner(
        predictor=predictor,
    )

    return runner.run(
        fixtures,
    )


def main() -> None:


    predictor = HistoricalMMIPredictor(
        state_repository=(
            HistoricalTeamStateRepository()
        ),
        rating_builder=(
            HistoricalRatingBuilder()
        ),
        league=League(
            name="Cyprus First Division",
            country="Cyprus",
            average_goals=2.65,
            home_advantage=1.06,
        ),
        prediction_engine=(
            PredictionEngine()
        ),
    )

    fixture_repository = (
        HistoricalFixtureRepository(
            filepath=(
                "data/historical_fixtures.json"
            ),
        )
    )

    report = run_backtest(
        repository=fixture_repository,
        predictor=predictor,
    )

    print()
    print("MMI STATIC-RATINGS BASELINE")
    print("-" * 60)
    print(
        f"Matches tested: "
        f"{report.total_matches}"
    )
    print(
        f"Correct predictions: "
        f"{report.correct_predictions}"
    )
    print(
        f"Accuracy: "
        f"{report.accuracy:.2%}"
    )
    print(
        f"Brier Score: "
        f"{report.brier_score:.6f}"
    )
    print(
        f"Log Loss: "
        f"{report.log_loss:.6f}"
    )
    print("-" * 60)
    print(
        "WARNING: This baseline uses static "
        "end-of-season ratings."
    )
    print(
        "It is not a leakage-free "
        "time-aware benchmark."
    )


if __name__ == "__main__":
    main()