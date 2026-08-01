from repositories.sportmonks_recent_form_repository import (
    SportmonksRecentFormRepository,
)


CYPRUS_SEASON_ID = 25996
PAFOS_TEAM_ID = 8119


def main() -> None:
    repository = (
        SportmonksRecentFormRepository(
            season_id=CYPRUS_SEASON_ID,
            matches_limit=5,
        )
    )

    recent_form = repository.get_for_team(
        team_id=PAFOS_TEAM_ID,
    )

    print()
    print("PAFOS RECENT FORM")
    print("-" * 50)
    print(f"Matches: {recent_form.matches}")
    print(
        f"Record: "
        f"{recent_form.wins}-"
        f"{recent_form.draws}-"
        f"{recent_form.losses}"
    )
    print(
        f"Goals: "
        f"{recent_form.goals_for}-"
        f"{recent_form.goals_against}"
    )


if __name__ == "__main__":
    main()