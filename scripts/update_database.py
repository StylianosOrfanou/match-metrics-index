from engines.rating_builder import (
    RatingBuilder,
)
from engines.rating_fusion_engine import (
    RatingFusionEngine,
)
from engines.recent_form_rating_builder import (
    RecentFormRatingBuilder,
)
from exporters.json_team_exporter import (
    JsonTeamExporter,
)
from repositories.json_league_repository import (
    JsonLeagueRepository,
)
from repositories.sportmonks_recent_form_repository import (
    SportmonksRecentFormRepository,
)
from repositories.sportmonks_team_statistics_repository import (
    SportmonksTeamStatisticsRepository,
)
from services.database_update_service import (
    DatabaseUpdateService,
)
from services.rating_pipeline_service import (
    RatingPipelineService,
)


CYPRUS_SEASON_ID = 25996
LEAGUE_NAME = "Cyprus First Division"

TEAM_IDS = {
    "AEK Larnaca": 726,
    "AEL": 611,
    "APOEL": 2604,
    "Akritas": 8171,
    "Anorthosis": 272,
    "Apollon": 6315,
    "Aris Limassol": 526,
    "Enosis": 2653,
    "Ethnikos Achna": 7608,
    "Krasava ENY Ypsonas FC": 28636,
    "Olympiakos": 562,
    "Omonia Aradippou": 8122,
    "Omonia": 368,
    "Pafos FC": 8119,
}


def main() -> None:
    print()
    print("MMI DATABASE UPDATE")
    print("-" * 70)

    league_repository = JsonLeagueRepository(
        file_path="data/leagues.json",
    )

    league = league_repository.get_league(
        LEAGUE_NAME,
    )

    statistics_repository = (
        SportmonksTeamStatisticsRepository(
            season_id=CYPRUS_SEASON_ID,
        )
    )

    recent_form_repository = (
        SportmonksRecentFormRepository(
            season_id=CYPRUS_SEASON_ID,
            matches_limit=5,
        )
    )

    rating_pipeline = RatingPipelineService(
        season_rating_builder=RatingBuilder(),
        recent_rating_builder=(
            RecentFormRatingBuilder()
        ),
        fusion_engine=RatingFusionEngine(),
    )

    exporter = JsonTeamExporter(
        file_path="data/teams.json",
    )

    update_service = DatabaseUpdateService(
        statistics_repository=(
            statistics_repository
        ),
        recent_form_repository=(
            recent_form_repository
        ),
        rating_pipeline=rating_pipeline,
        exporter=exporter,
        team_ids=TEAM_IDS,
        teams_file_path="data/teams.json",
        backup_directory=(
            "data/backups/teams"
        ),
    )

    summary = update_service.update(
        league=league,
    )

    print()
    print("-" * 70)
    print("UPDATE SUMMARY")
    print("-" * 70)

    print(
        f"Season statistics: "
        f"{summary.statistics_loaded}"
    )

    print(
        f"Recent forms: "
        f"{summary.recent_forms_loaded}"
    )

    print(
        f"Teams exported: "
        f"{summary.teams_exported}"
    )

    if summary.backup_path is None:
        print("Backup: Not required")
    else:
        print(
            f"Backup: "
            f"{summary.backup_path}"
        )

    print("-" * 70)
    print("DATABASE UPDATE COMPLETED")


if __name__ == "__main__":
    main()