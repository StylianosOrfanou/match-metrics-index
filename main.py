from engines.prediction_engine import PredictionEngine

from presentation.terminal_presenter import (
    display_prediction,
)

from repositories.json_league_repository import (
    JsonLeagueRepository,
)

from repositories.json_team_repository import (
    JsonTeamRepository,
)

from services.match_service import MatchService


def main():
    league_repository = JsonLeagueRepository(
        file_path="data/leagues.json",
    )

    team_repository = JsonTeamRepository(
        file_path="data/teams.json",
        league_repository=league_repository,
    )

    match_service = MatchService(team_repository)

    match = match_service.create_match(
        home_team_name="Pafos FC",
        away_team_name="Omonia",
    )

    prediction_engine = PredictionEngine()
    prediction = prediction_engine.predict(match)

    display_prediction(prediction)


if __name__ == "__main__":
    main()