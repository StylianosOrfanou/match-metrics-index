import json
from pathlib import Path

from models.league import League
from repositories.league_repository import LeagueRepository


class JsonLeagueRepository(LeagueRepository):

    def __init__(self, file_path: str):
        self._file_path = Path(file_path)
        self._leagues = {}
        self._load_leagues()

    def _load_leagues(self):
        if not self._file_path.exists():
            raise FileNotFoundError(
                f"Leagues file was not found: {self._file_path}"
            )

        with self._file_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            leagues_data = json.load(file)

        for league_data in leagues_data:
            league = League(
                name=league_data["name"],
                country=league_data["country"],
                average_goals=league_data["average_goals"],
                home_advantage=league_data["home_advantage"],
            )

            self._leagues[league.name] = league

    def get_league(self, name: str) -> League:
        if name not in self._leagues:
            raise ValueError(
                f"League '{name}' was not found."
            )

        return self._leagues[name]