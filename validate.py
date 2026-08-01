from engines.prediction_engine import PredictionEngine

from repositories.json_league_repository import (
    JsonLeagueRepository,
)
from repositories.json_team_repository import (
    JsonTeamRepository,
)
from repositories.sportmonks_validation_repository import (
    SportmonksValidationRepository,
)

from services.match_service import MatchService

from validation.validation_metrics import ValidationMetrics
from validation.validation_report import ValidationReport
from validation.validator import Validator


CYPRUS_SEASON_ID = 25996


def main() -> None:
    league_repository = JsonLeagueRepository(
        file_path="data/leagues.json",
    )

    team_repository = JsonTeamRepository(
        file_path="data/teams.json",
        league_repository=league_repository,
    )

    validation_repository = SportmonksValidationRepository(
        season_id=CYPRUS_SEASON_ID,
        limit=10,
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

    print()
    print(f"Validation matches loaded: {len(matches)}")
    print()

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