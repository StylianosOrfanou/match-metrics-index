from clients.sportmonks_client import SportmonksClient


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

    season_response = client.get(
        f"seasons/{CYPRUS_SEASON_ID}",
        params={
            "include": (
                "fixtures.participants;"
                "fixtures.scores"
            ),
        },
    )

    season = season_response["data"]

    fixtures = season.get(
        "fixtures",
        [],
    )

    print("\nCYPRUS FIXTURE AUDIT")
    print("-" * 70)
    print(f"Season: {season.get('name')}")
    print(f"Fixtures returned: {len(fixtures)}")
    print("-" * 70)

    fixtures.sort(
        key=lambda fixture: fixture.get(
            "starting_at",
            "",
        )
    )

    # Τυπώνουμε μόνο 5 fixtures.
    for fixture in fixtures[:5]:
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
            f"{fixture.get('id')} | "
            f"{fixture.get('starting_at')} | "
            f"{home_team} "
            f"{home_score}-{away_score} "
            f"{away_team}"
        )

    if not fixtures:
        print("\nNo fixtures available for odds audit.")
        return

    # Το odds audit είναι ΕΞΩ από το fixture loop.
    test_fixture = fixtures[0]
    test_fixture_id = test_fixture["id"]

    print("\nODDS ACCESS AUDIT")
    print("-" * 70)
    print(f"Fixture ID: {test_fixture_id}")

    try:
        odds_response = client.get(
            f"odds/pre-match/fixtures/{test_fixture_id}",
            params={
                "include": "bookmaker",
            },
        )

        print("Odds request completed.")

        odds = odds_response.get(
            "data",
            [],
        )

        print(f"Odds returned: {len(odds)}")

        # <<< ΒΑΖΕΙΣ ΤΟΝ ΚΩΔΙΚΑ ΕΔΩ >>>

        bookmakers = {}

        for odd in odds:
            bookmaker = odd.get("bookmaker")

            if bookmaker:
                bookmakers[
                    bookmaker["id"]
                ] = bookmaker["name"]

        print("\nBOOKMAKERS")
        print("-" * 70)

        for bookmaker_id, name in sorted(
            bookmakers.items()
        ):
            print(f"{bookmaker_id}: {name}")

    except Exception as error:
        print(type(error).__name__)
        print(error)


if __name__ == "__main__":
    main()