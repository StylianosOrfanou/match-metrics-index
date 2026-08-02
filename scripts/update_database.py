from engines.rating_builder import (
    RatingBuilder,
)

from engines.recent_form_rating_builder import (
    RecentFormRatingBuilder,
)
from engines.weighted_rating_engine import WeightedRatingEngine
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

from engines.elo_engine import EloEngine
from engines.rating_normalizer import (
    RatingNormalizer,
)
from repositories.sportmonks_elo_repository import (
    SportmonksEloRepository,
)
from services.elo_builder_service import (
    EloBuilderService,
)
from services.elo_service import EloService
from services.team_signal_factory import TeamSignalFactory
from services.team_signal_factory import TeamSignalFactory

from engines.weighted_rating_engine import (
    WeightedRatingEngine,
)

from services.team_signal_factory import (
    TeamSignalFactory,
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
        weighted_rating_engine=WeightedRatingEngine(),
        signal_factory=TeamSignalFactory(),
    )

    elo_repository = SportmonksEloRepository(
        season_id=CYPRUS_SEASON_ID,
    )

    elo_builder = EloBuilderService(
        elo_engine=EloEngine(
            k_factor=32,
            home_advantage=100,
        ),
        default_rating=1500,
    )

    elo_service = EloService(
        repository=elo_repository,
        builder=elo_builder,
        normalizer=RatingNormalizer(),
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
        rating_pipeline = RatingPipelineService(
            season_rating_builder=RatingBuilder(),
            recent_rating_builder=RecentFormRatingBuilder(),
            weighted_rating_engine=WeightedRatingEngine(),
            signal_factory=TeamSignalFactory(),
        ),
        exporter=exporter,
        team_ids=TEAM_IDS,
        teams_file_path="data/teams.json",
        backup_directory=(
            "data/backups/teams"
        ),
        elo_service=elo_service,
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