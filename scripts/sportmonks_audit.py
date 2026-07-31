from clients.sportmonks_client import (
    SportmonksClient,
)


CYPRUS_SEASON_ID = 25996


def get_team_name(
    fixture: dict,
    location: str,
) -> str:
    participants = fixture.get(
        "participants",
        [],
    )

    for participant in participants:
        meta = participant.get(
            "meta",
            {},
        )

        if meta.get("location") == location:
            return participant.get(
                "name",
                "Unknown",
            )

    return "Unknown"


def get_current_score(
    fixture: dict,
    participant: str,
) -> int | None:
    scores = fixture.get(
        "scores",
        [],
    )

    for score in scores:
        if score.get("description") != "CURRENT":
            continue

        score_data = score.get(
            "score",
            {},
        )

        if score_data.get("participant") == participant:
            return score_data.get("goals")

    return None


def main() -> None:
    client = SportmonksClient()

    response = client.get(
        f"seasons/{CYPRUS_SEASON_ID}",
        params={
            "include": (
                "fixtures.participants;"
                "fixtures.scores"
            ),
        },
    )

    season = response["data"]

    fixtures = season.get(
        "fixtures",
        [],
    )

    print("\nCYPRUS FIXTURE AUDIT")
    print("-" * 70)
    print(f"Season: {season['name']}")
    print(f"Fixtures returned: {len(fixtures)}")
    print("-" * 70)

    fixtures.sort(
        key=lambda fixture: fixture["starting_at"]
    )
    
    for fixture in fixtures:
        home_team = get_team_name(
            fixture,
            "home",
        )

        away_team = get_team_name(
            fixture,
            "away",
        )

        home_score = get_current_score(
            fixture,
            "home",
        )

        away_score = get_current_score(
            fixture,
            "away",
        )

        print(
            f"{fixture['id']} | "
            f"{fixture['starting_at']} | "
            f"{home_team} "
            f"{home_score}-{away_score} "
            f"{away_team}"
        )


if __name__ == "__main__":
    main()