import json
import shutil
from datetime import datetime
from pathlib import Path

from builders.team_builder import TeamBuilder
from exporters.json_team_exporter import JsonTeamExporter
from models.league import League
from models.rating_change import RatingChange
from repositories.sportmonks_team_statistics_repository import (
    SportmonksTeamStatisticsRepository,
)


class TeamRatingUpdateService:

    RATING_FIELDS = (
        "attack_rating",
        "defence_rating",
        "form_rating",
        "home_strength",
        "away_strength",
    )

    def __init__(
        self,
        statistics_repository:
        SportmonksTeamStatisticsRepository,
        team_builder: TeamBuilder,
        exporter: JsonTeamExporter,
        teams_file_path: str,
        backup_directory: str,
    ) -> None:
        self._statistics_repository = (
            statistics_repository
        )
        self._team_builder = team_builder
        self._exporter = exporter
        self._teams_file_path = Path(
            teams_file_path
        )
        self._backup_directory = Path(
            backup_directory
        )

    def update(
        self,
        league: League,
    ) -> list[RatingChange]:
        old_data = self._load_existing_teams()

        statistics = (
            self._statistics_repository.get_all()
        )

        teams = self._team_builder.build(
            statistics=statistics,
            league=league,
        )

        self._create_backup()

        self._exporter.export(
            teams
        )

        return self._calculate_changes(
            old_data=old_data,
            teams=teams,
        )

    def _load_existing_teams(
        self,
    ) -> dict[str, dict]:
        if not self._teams_file_path.exists():
            return {}

        data = json.loads(
            self._teams_file_path.read_text(
                encoding="utf-8",
            )
        )

        return {
            team["name"]: team
            for team in data
        }

    def _create_backup(self) -> None:
        if not self._teams_file_path.exists():
            return

        self._backup_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_path = (
            self._backup_directory
            / f"teams_{timestamp}.json"
        )

        shutil.copy2(
            self._teams_file_path,
            backup_path,
        )

    def _calculate_changes(
        self,
        old_data: dict[str, dict],
        teams: list,
    ) -> list[RatingChange]:
        changes: list[RatingChange] = []

        for team in teams:
            previous = old_data.get(
                team.name
            )

            if previous is None:
                continue

            for field in self.RATING_FIELDS:
                old_value = float(
                    previous[field]
                )

                new_value = float(
                    getattr(team, field)
                )

                if old_value == new_value:
                    continue

                changes.append(
                    RatingChange(
                        team_name=team.name,
                        metric=field,
                        old_value=old_value,
                        new_value=new_value,
                    )
                )

        return changes
