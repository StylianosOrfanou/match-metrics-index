import json
from pathlib import Path
from repositories.league_repository import LeagueRepository
from models.team import Team
from repositories.team_repository import TeamRepository


class JsonTeamRepository(TeamRepository):

    def __init__(
        self,
        file_path: str,
        league_repository: LeagueRepository,
    ):
        self._file_path = Path(file_path)
        self._league_repository = league_repository
        self._teams = {}
        self._load_teams()

    def _load_teams(self):
        if not self._file_path.exists():
            raise FileNotFoundError(
                f"Teams file was not found: {self._file_path}"
            )

        with self._file_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            teams_data = json.load(file)

        for team_data in teams_data:
            league = self._league_repository.get_league(
                team_data["league"]
            )

            team = Team(
                name=team_data["name"],
                league=league,
                attack_rating=team_data["attack_rating"],
                defence_rating=team_data["defence_rating"],
                form_rating=team_data["form_rating"],
            )

            self._teams[team.name] = team

    def get_team(self, name: str) -> Team:
        if name not in self._teams:
            raise ValueError(
                f"Team '{name}' was not found."
            )

        return self._teams[name]