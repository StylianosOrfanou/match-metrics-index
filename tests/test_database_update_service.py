from pathlib import Path

from engines.rating_builder import (
    TeamSeasonStatistics,
)
from exporters.json_team_exporter import (
    JsonTeamExporter,
)
from models.league import League
from models.recent_form import RecentForm
from services.database_update_service import (
    DatabaseUpdateService,
)
from services.rating_pipeline_service import (
    RatingPipelineService,
)


league = League(
    name="Cyprus First Division",
    country="Cyprus",
    average_goals=2.65,
    home_advantage=1.06,
)


class FakeStatisticsRepository:

    def get_all(
        self,
    ) -> list[TeamSeasonStatistics]:
        return [
            TeamSeasonStatistics(
                name="Strong Team",
                goals_for_per_game=2.0,
                goals_against_per_game=0.8,
                home_goals_for_per_game=2.2,
                away_goals_for_per_game=1.8,
                home_goals_against_per_game=0.6,
                away_goals_against_per_game=1.0,
                shots_per_game=14.0,
                xg_per_game=1.8,
                wins=20,
                draws=5,
                losses=5,
            ),
            TeamSeasonStatistics(
                name="Weak Team",
                goals_for_per_game=0.8,
                goals_against_per_game=2.0,
                home_goals_for_per_game=1.0,
                away_goals_for_per_game=0.6,
                home_goals_against_per_game=1.8,
                away_goals_against_per_game=2.2,
                shots_per_game=7.0,
                xg_per_game=0.7,
                wins=4,
                draws=5,
                losses=21,
            ),
        ]


class FakeRecentFormRepository:

    def get_for_team(
        self,
        team_id: int,
    ) -> RecentForm:
        if team_id == 1:
            return RecentForm(
                matches=5,
                wins=4,
                draws=1,
                losses=0,
                goals_for=11,
                goals_against=3,
                home_matches=3,
                home_goals_for=7,
                home_goals_against=1,
                away_matches=2,
                away_goals_for=4,
                away_goals_against=2,
                expected_goals=0.0,
                shots=0,
            )

        return RecentForm(
            matches=5,
            wins=0,
            draws=1,
            losses=4,
            goals_for=3,
            goals_against=11,
            home_matches=3,
            home_goals_for=2,
            home_goals_against=7,
            away_matches=2,
            away_goals_for=1,
            away_goals_against=4,
            expected_goals=0.0,
            shots=0,
        )


def test_update_exports_all_teams(
    tmp_path,
):
    teams_path = tmp_path / "teams.json"
    backup_directory = tmp_path / "backups"

    service = DatabaseUpdateService(
        statistics_repository=(
            FakeStatisticsRepository()
        ),
        recent_form_repository=(
            FakeRecentFormRepository()
        ),
        rating_pipeline=(
            RatingPipelineService()
        ),
        exporter=JsonTeamExporter(
            file_path=str(teams_path),
        ),
        team_ids={
            "Strong Team": 1,
            "Weak Team": 2,
        },
        teams_file_path=str(teams_path),
        backup_directory=str(
            backup_directory
        ),
    )

    summary = service.update(
        league=league,
    )

    assert teams_path.exists()
    assert summary.statistics_loaded == 2
    assert summary.recent_forms_loaded == 2
    assert summary.teams_exported == 2


def test_update_creates_backup_when_file_exists(
    tmp_path,
):
    teams_path = tmp_path / "teams.json"
    teams_path.write_text(
        "[]",
        encoding="utf-8",
    )

    backup_directory = tmp_path / "backups"

    service = DatabaseUpdateService(
        statistics_repository=(
            FakeStatisticsRepository()
        ),
        recent_form_repository=(
            FakeRecentFormRepository()
        ),
        rating_pipeline=(
            RatingPipelineService()
        ),
        exporter=JsonTeamExporter(
            file_path=str(teams_path),
        ),
        team_ids={
            "Strong Team": 1,
            "Weak Team": 2,
        },
        teams_file_path=str(teams_path),
        backup_directory=str(
            backup_directory
        ),
    )

    summary = service.update(
        league=league,
    )

    assert summary.backup_path is not None
    assert summary.backup_path.exists()
    assert (
        summary.backup_path.parent
        == backup_directory
    )


def test_update_skips_backup_when_file_missing(
    tmp_path,
):
    teams_path = tmp_path / "teams.json"

    service = DatabaseUpdateService(
        statistics_repository=(
            FakeStatisticsRepository()
        ),
        recent_form_repository=(
            FakeRecentFormRepository()
        ),
        rating_pipeline=(
            RatingPipelineService()
        ),
        exporter=JsonTeamExporter(
            file_path=str(teams_path),
        ),
        team_ids={
            "Strong Team": 1,
            "Weak Team": 2,
        },
        teams_file_path=str(teams_path),
        backup_directory=str(
            tmp_path / "backups"
        ),
    )

    summary = service.update(
        league=league,
    )

    assert summary.backup_path is None