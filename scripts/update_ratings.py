from builders.team_builder import TeamBuilder
from engines.rating_builder import RatingBuilder
from exporters.json_team_exporter import JsonTeamExporter
from repositories.json_league_repository import (
    JsonLeagueRepository,
)
from repositories.sportmonks_team_statistics_repository import (
    SportmonksTeamStatisticsRepository,
)
from services.team_rating_update_service import (
    TeamRatingUpdateService,
)


CYPRUS_SEASON_ID = 25996
LEAGUE_NAME = "Cyprus First Division"


METRIC_LABELS = {
    "attack_rating": "Attack",
    "defence_rating": "Defence",
    "form_rating": "Form",
    "home_strength": "Home Strength",
    "away_strength": "Away Strength",
}


def main() -> None:
    print()
    print("MMI WEEKLY RATINGS UPDATE")
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

    team_builder = TeamBuilder(
        rating_builder=RatingBuilder(),
    )

    exporter = JsonTeamExporter(
        file_path="data/teams.json",
    )

    update_service = TeamRatingUpdateService(
        statistics_repository=statistics_repository,
        team_builder=team_builder,
        exporter=exporter,
        teams_file_path="data/teams.json",
        backup_directory="data/backups/teams",
    )

    changes = update_service.update(
        league=league,
    )

    print()
    print("-" * 70)
    print("RATING CHANGES")
    print("-" * 70)

    if not changes:
        print("No rating changes detected.")
    else:
        current_team = None

        for change in changes:
            if change.team_name != current_team:
                if current_team is not None:
                    print()

                current_team = change.team_name
                print(change.team_name)

            label = METRIC_LABELS.get(
                change.metric,
                change.metric,
            )

            sign = (
                "+"
                if change.difference > 0
                else ""
            )

            print(
                f"  {label}: "
                f"{change.old_value:.2f} → "
                f"{change.new_value:.2f} "
                f"({sign}{change.difference:.2f})"
            )

    print()
    print("-" * 70)
    print("Weekly update completed.")
    print("data/teams.json updated.")
    print(
        "Backup saved in "
        "data/backups/teams/"
    )


if __name__ == "__main__":
    main()