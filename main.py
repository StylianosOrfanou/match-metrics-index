from engines.prediction_engine import PredictionEngine

from presentation.terminal_presenter import (
    display_prediction,
)

from repositories.json_team_repository import (
    JsonTeamRepository,
)

from services.match_service import MatchService


def main():
    repository = JsonTeamRepository(
        file_path="data/teams.json"
    )
    match_service = MatchService(repository)

    match = match_service.create_match(
        home_team_name="Pafos FC",
        away_team_name="Omonia",
    )

    prediction_engine = PredictionEngine()
    prediction = prediction_engine.predict(match)
    display_prediction(prediction)


if __name__ == "__main__":
    main()