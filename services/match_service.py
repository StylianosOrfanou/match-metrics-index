from models.match import Match
from repositories.team_repository import TeamRepository


class MatchService:

    def __init__(self, team_repository: TeamRepository):
        self._team_repository = team_repository

    def create_match(
        self,
        home_team_name: str,
        away_team_name: str,
    ) -> Match:

        home_team = self._team_repository.get_team(
            home_team_name
        )

        away_team = self._team_repository.get_team(
            away_team_name
        )

        return Match(
            home_team=home_team,
            away_team=away_team,
        )