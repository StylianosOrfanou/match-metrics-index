from engines.prediction_engine import (
    PredictionEngine,
)

from repositories.json_league_repository import (
    JsonLeagueRepository,
)

from repositories.json_team_repository import (
    JsonTeamRepository,
)

from repositories.json_validation_repository import (
    JsonValidationRepository,
)

from services.match_service import (
    MatchService,
)

from validation.validation_metrics import (
    ValidationMetrics,
)

from validation.validation_report import (
    ValidationReport,
)

from validation.validator import (
    Validator,
)


def main() -> None:
    league_repository = JsonLeagueRepository(
        file_path="data/leagues.json",
    )

    team_repository = JsonTeamRepository(
        file_path="data/teams.json",
        league_repository=league_repository,
    )

    validation_repository = JsonValidationRepository(
        file_path="data/validation_matches.json",
    )

    match_service = MatchService(
        team_repository,
    )

    prediction_engine = PredictionEngine()

    validator = Validator(
        match_service=match_service,
        prediction_engine=prediction_engine,
    )

    matches = validation_repository.get_all()

    results = validator.validate(
        matches,
    )

    metrics = ValidationMetrics(
        results,
    )

    report = ValidationReport(
        metrics,
    )

    report.display()


if __name__ == "__main__":
    main()