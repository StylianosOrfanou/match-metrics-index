from clients.sportmonks_client import (
    SportmonksClient,
)


CYPRUS_SEASON_ID = 25996


def main() -> None:
    client = SportmonksClient()

    response = client.get(
        f"teams/seasons/{CYPRUS_SEASON_ID}",
    )

    teams = response.get(
        "data",
        [],
    )

    teams.sort(
        key=lambda team: team.get(
            "name",
            "",
        )
    )

    print("\nCYPRUS TEAMS AUDIT")
    print("-" * 70)
    print(f"Season ID: {CYPRUS_SEASON_ID}")
    print(f"Teams returned: {len(teams)}")
    print("-" * 70)

    for team in teams:
        print(
            f"{team.get('id')} | "
            f"{team.get('name')} | "
            f"Short code: {team.get('short_code')}"
        )

    pagination = response.get(
        "pagination",
        {},
    )

    print("\nPAGINATION")
    print("-" * 70)
    print(
        f"Count: {pagination.get('count')}"
    )
    print(
        f"Has more: {pagination.get('has_more')}"
    )


if __name__ == "__main__":
    main()