from builders.team_builder import TeamBuilder
from engines.rating_builder import RatingBuilder
from exporters.json_team_exporter import JsonTeamExporter
from repositories.json_league_repository import (
    JsonLeagueRepository,
)
from repositories.sportmonks_team_statistics_repository import (
    SportmonksTeamStatisticsRepository,
)


CYPRUS_SEASON_ID = 25996
LEAGUE_NAME = "Cyprus First Division"


def main() -> None:
    print("\nBUILDING MMI TEAMS")
    print("-" * 70)

    league_repository = JsonLeagueRepository(
        file_path="data/leagues.json",
    )

    league = league_repository.get_league(
        LEAGUE_NAME,
    )

    print("Loading Sportmonks statistics...")

    statistics_repository = (
        SportmonksTeamStatisticsRepository(
            season_id=CYPRUS_SEASON_ID,
        )
    )

    statistics = statistics_repository.get_all()

    print(
        f"Statistics loaded: {len(statistics)} teams"
    )

    print("Calculating ratings...")

    rating_builder = RatingBuilder()

    team_builder = TeamBuilder(
        rating_builder=rating_builder,
    )

    teams = team_builder.build(
        statistics=statistics,
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
        teams,
    )

    print("-" * 70)
    print(
        f"SUCCESS: {len(teams)} teams exported."
    )
    print("data/teams.json updated.")


if __name__ == "__main__":
    main()