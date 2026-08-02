import shutil
from datetime import datetime
from pathlib import Path

from exporters.json_team_exporter import (
    JsonTeamExporter,
)
from models.database_update_summary import (
    DatabaseUpdateSummary,
)
from models.league import League
from repositories.sportmonks_recent_form_repository import (
    SportmonksRecentFormRepository,
)
from repositories.sportmonks_team_statistics_repository import (
    SportmonksTeamStatisticsRepository,
)
from services.rating_pipeline_service import (
    RatingPipelineService,
)

from services.elo_service import EloService


class DatabaseUpdateService:

    def __init__(
        self,
        statistics_repository:
        SportmonksTeamStatisticsRepository,
        recent_form_repository:
        SportmonksRecentFormRepository,
        rating_pipeline: RatingPipelineService,
        exporter: JsonTeamExporter,
        team_ids: dict[str, int],
        teams_file_path: str,
        backup_directory: str,
        elo_service: EloService | None = None,
    ) -> None:
        self._statistics_repository = (
            statistics_repository
        )
        self._recent_form_repository = (
            recent_form_repository
        )
        self._rating_pipeline = rating_pipeline
        self._exporter = exporter
        self._team_ids = team_ids

        self._teams_file_path = Path(
            teams_file_path
        )

        self._backup_directory = Path(
            backup_directory
        )
        self._elo_service = elo_service

    def update(
        self,
        league: League,
    ) -> DatabaseUpdateSummary:
        season_statistics = (
            self._statistics_repository.get_all()
        )

        recent_forms = self._load_recent_forms()
        elo_ratings = {}

        if self._elo_service is not None:
            elo_ratings = self._elo_service.build()

        teams = self._rating_pipeline.build(
            season_statistics=season_statistics,
            recent_forms=recent_forms,
            league=league,
            elo_ratings=elo_ratings,
        )

        backup_path = self._create_backup()

        self._exporter.export(
            teams
        )

        return DatabaseUpdateSummary(
            statistics_loaded=len(
                season_statistics
            ),
            recent_forms_loaded=len(
                recent_forms
            ),
            teams_exported=len(teams),
            backup_path=backup_path,
        )

    def _load_recent_forms(self) -> dict:
        recent_forms = {}

        for team_name, team_id in (
            self._team_ids.items()
        ):
            recent_forms[team_name] = (
                self._recent_form_repository
                .get_for_team(
                    team_id=team_id,
                )
            )

        return recent_forms

    def _create_backup(
        self,
    ) -> Path | None:
        if not self._teams_file_path.exists():
            return None

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

        return backup_path