from engines.rating_builder import RatingBuilder

from engines.recent_form_rating_builder import (
    RecentFormRatingBuilder,
)

from engines.weighted_rating_engine import (
    WeightedRatingEngine,
)

from services.team_signal_factory import (
    TeamSignalFactory,
)

from exporters.json_team_exporter import JsonTeamExporter

from repositories.json_league_repository import (
    JsonLeagueRepository,
)
from repositories.sportmonks_recent_form_repository import (
    SportmonksRecentFormRepository,
)
from repositories.sportmonks_team_statistics_repository import (
    SportmonksTeamStatisticsRepository,
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
    print("BUILDING MMI TEAMS")
    print("-" * 70)

    league_repository = JsonLeagueRepository(
        file_path="data/leagues.json",
    )

    league = league_repository.get_league(
        LEAGUE_NAME,
    )

    print("Loading season statistics...")

    statistics_repository = (
        SportmonksTeamStatisticsRepository(
            season_id=CYPRUS_SEASON_ID,
        )
    )

    season_statistics = (
        statistics_repository.get_all()
    )

    print(
        f"Season statistics loaded: "
        f"{len(season_statistics)} teams"
    )

    print()
    print("Loading recent form...")

    recent_repository = (
        SportmonksRecentFormRepository(
            season_id=CYPRUS_SEASON_ID,
            matches_limit=5,
        )
    )

    recent_forms = {}

    for index, (
        team_name,
        team_id,
    ) in enumerate(
        TEAM_IDS.items(),
        start=1,
    ):
        print(
            f"Loading recent form "
            f"{index}/{len(TEAM_IDS)}: "
            f"{team_name}"
        )

        recent_forms[team_name] = (
            recent_repository.get_for_team(
                team_id=team_id,
            )
        )

    print(
        f"Recent forms loaded: "
        f"{len(recent_forms)} teams"
    )

    print()
    print("Building final fused ratings...")

    pipeline = RatingPipelineService(
        season_rating_builder=RatingBuilder(),
        recent_rating_builder=(
            RecentFormRatingBuilder()
        ),
        weighted_rating_engine=(
            WeightedRatingEngine()
        ),
        signal_factory=TeamSignalFactory(),
    )

    teams = pipeline.build(
        season_statistics=season_statistics,
        recent_forms=recent_forms,
        league=league,
    )

    print(
        f"Team objects created: {len(teams)}"
    )

    print("Writing data/teams.json...")

    exporter = JsonTeamExporter(
        file_path="data/teams.json",
    )

    exporter.export(
        teams
    )

    print("-" * 70)
    print(
        f"SUCCESS: {len(teams)} teams exported."
    )
    print(
        "Season and recent-form ratings fused."
    )
    print("data/teams.json updated.")


if __name__ == "__main__":
    main()