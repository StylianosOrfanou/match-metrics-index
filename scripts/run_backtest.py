from engines.prediction_engine import (
    PredictionEngine,
)
from repositories.json_league_repository import (
    JsonLeagueRepository,
)
from repositories.json_team_repository import (
    JsonTeamRepository,
)
from services.match_service import (
    MatchService,
)
from validation.backtest_runner import (
    BacktestRunner,
)
from validation.historical_fixture_repository import (
    HistoricalFixtureRepository,
)
from validation.mmi_time_aware_predictor import (
    MMITimeAwarePredictor,
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
    league_repository = JsonLeagueRepository(
        file_path="data/leagues.json",
    )

    team_repository = JsonTeamRepository(
        file_path="data/teams.json",
        league_repository=league_repository,
    )

    match_service = MatchService(
        team_repository=team_repository,
    )

    predictor = MMITimeAwarePredictor(
        match_service=match_service,
        prediction_engine=PredictionEngine(),
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