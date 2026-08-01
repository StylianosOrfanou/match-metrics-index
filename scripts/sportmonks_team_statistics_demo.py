from repositories.sportmonks_team_statistics_repository import (
    SportmonksTeamStatisticsRepository,
)


CYPRUS_SEASON_ID = 25996


def main() -> None:
    repository = (
        SportmonksTeamStatisticsRepository(
            season_id=CYPRUS_SEASON_ID,
        )
    )

    teams = repository.get_all()

    print()
    print("TEAM SEASON STATISTICS")
    print("-" * 100)
    print(f"Teams created: {len(teams)}")
    print("-" * 100)

    for team in teams:
        print(
            f"{team.name:<28} | "
            f"GF {team.goals_for_per_game:>4.2f} | "
            f"GA {team.goals_against_per_game:>4.2f} | "
            f"Shots {team.shots_per_game:>5.2f} | "
            f"xG {team.xg_per_game:>4.2f} | "
            f"W-D-L "
            f"{team.wins}-"
            f"{team.draws}-"
            f"{team.losses}"
        )


if __name__ == "__main__":
    main()