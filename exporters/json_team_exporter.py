import json
from pathlib import Path

from models.team import Team


class JsonTeamExporter:

    def __init__(
        self,
        file_path: str,
    ) -> None:
        self._file_path = Path(
            file_path
        )

    def export(
        self,
        teams: list[Team],
    ) -> None:
        if not teams:
            raise ValueError(
                "At least one team is required."
            )

        data = [
            self._team_to_dict(team)
            for team in teams
        ]

        self._file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary_path = (
            self._file_path.with_suffix(
                ".tmp"
            )
        )

        temporary_path.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        temporary_path.replace(
            self._file_path
        )

    @staticmethod
    def _team_to_dict(
        team: Team,
    ) -> dict:
        return {
            "name": team.name,
            "league": team.league.name,
            "attack_rating": (
                team.attack_rating
            ),
            "defence_rating": (
                team.defence_rating
            ),
            "form_rating": (
                team.form_rating
            ),
            "home_strength": (
                team.home_strength
            ),
            "away_strength": (
                team.away_strength
            ),
        }