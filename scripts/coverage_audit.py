import os
from pathlib import Path
from typing import Any
import time
import requests
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"


def api_get(
    endpoint: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not API_KEY:
        raise RuntimeError(
            "Το API_FOOTBALL_KEY δεν βρέθηκε στο .env"
        )

    response = requests.get(
        f"{BASE_URL}/{endpoint}",
        headers={
            "x-apisports-key": API_KEY,
        },
        params=params or {},
        timeout=20,
    )

    if response.status_code == 429:
        print("Rate limit reached. Waiting 60 seconds...")
        time.sleep(60)

        response = requests.get(
            f"{BASE_URL}/{endpoint}",
            headers={
                "x-apisports-key": API_KEY,
            },
            params=params or {},
            timeout=20,
        )

    response.raise_for_status()
    data = response.json()

    errors = data.get("errors")

    if errors:
        raise RuntimeError(f"API error: {errors}")

    return data



def print_fixture_summary(
    fixture: dict[str, Any],
) -> None:
    fixture_info = fixture.get("fixture", {})
    league = fixture.get("league", {})
    teams = fixture.get("teams", {})
    goals = fixture.get("goals", {})

    print()
    print(f"Fixture ID: {fixture_info.get('id')}")
    print(
        f"{teams.get('home', {}).get('name')} "
        f"{goals.get('home')} - "
        f"{goals.get('away')} "
        f"{teams.get('away', {}).get('name')}"
    )
    print(f"Date: {fixture_info.get('date')}")
    print(
        "Status: "
        f"{fixture_info.get('status', {}).get('long')}"
    )
    print(f"Season: {league.get('season')}")


def audit_fixture_details(
    fixture_id: int,
) -> None:
    print("\n" + "=" * 50)
    print(f"AUDITING FIXTURE {fixture_id}")
    print("=" * 50)

    endpoints = {
        "Statistics": (
            "fixtures/statistics",
            {"fixture": fixture_id},
        ),
        "Lineups": (
            "fixtures/lineups",
            {"fixture": fixture_id},
        ),
        "Player statistics": (
            "fixtures/players",
            {"fixture": fixture_id},
        ),
        "Events": (
            "fixtures/events",
            {"fixture": fixture_id},
        ),
    }

    for label, (endpoint, params) in endpoints.items():
        data = api_get(endpoint, params)
        results = data.get("results", 0)
        api_response = data.get("response", [])

        print()
        print(f"{label}:")
        print(f"Results: {results}")
        print(
            "Available: "
            f"{'YES' if api_response else 'NO'}"
        )


def main() -> None:
    print("API-FOOTBALL COVERAGE AUDIT")
    print("-" * 40)

    status_data = api_get("status")
    account = status_data["response"]

    print(
        "Account: "
        f"{account.get('account', {}).get('firstname', 'Unknown')}"
    )
    print(
        "Plan: "
        f"{account.get('subscription', {}).get('plan', 'Unknown')}"
    )
    print(
        "Requests today: "
        f"{account.get('requests', {}).get('current', 0)} / "
        f"{account.get('requests', {}).get('limit_day', 0)}"
    )

    print("\nSearching for Cyprus leagues...")

    leagues_data = api_get(
        "leagues",
        {
            "country": "Cyprus",
        },
    )

    leagues = leagues_data.get("response", [])

    if not leagues:
        print("Δεν βρέθηκαν διοργανώσεις για την Κύπρο.")
        return

    for item in leagues:
        league = item.get("league", {})
        country = item.get("country", {})
        seasons = item.get("seasons", [])

        season_years = [
            season.get("year")
            for season in seasons
            if season.get("year") is not None
        ]

        print()
        print(f"League ID: {league.get('id')}")
        print(f"League: {league.get('name')}")
        print(f"Type: {league.get('type')}")
        print(f"Country: {country.get('name')}")
        print(f"Available seasons: {season_years}")

    print(
        "\nSearching for recent Cyprus "
        "1. Division fixtures..."
    )

    fixtures_data = api_get(
        "fixtures",
        {
            "league": 318,
            "season": 2024,
        },
    )

    fixtures = fixtures_data.get("response", [])

    fixtures.sort(
        key=lambda item: item.get("fixture", {}).get("timestamp", 0),
        reverse=True,
    )

    fixtures = fixtures[:10]

    if not fixtures:
        print("No fixtures found.")
        return

    print(f"Fixtures found: {len(fixtures)}")

    for fixture in fixtures:
        print_fixture_summary(fixture)

    completed_fixtures = [
        fixture
        for fixture in fixtures
        if fixture.get("fixture", {})
        .get("status", {})
        .get("short") in {"FT", "AET", "PEN"}
    ]

    if not completed_fixtures:
        print(
            "\nNo completed fixture found "
            "for detailed audit."
        )
        return

    coverage = {
        "Statistics": 0,
        "Lineups": 0,
        "Player statistics": 0,
        "Events": 0,
    }

    endpoints = {
        "Statistics": "fixtures/statistics",
        "Lineups": "fixtures/lineups",
        "Player statistics": "fixtures/players",
        "Events": "fixtures/events",
    }

    print("\n" + "=" * 50)
    print("10-MATCH COVERAGE SUMMARY")
    print("=" * 50)

    for fixture in completed_fixtures[:10]:
        fixture_id = fixture["fixture"]["id"]

        print(f"\nFixture {fixture_id}")

        for label, endpoint in endpoints.items():
            data = api_get(
                endpoint,
                {
                    "fixture": fixture_id,
                },
            )

            time.sleep(7)

            available = bool(data.get("response", []))

            if available:
                coverage[label] += 1

            print(
                f"{label}: "
                f"{'YES' if available else 'NO'}"
            )

    print("\n" + "=" * 50)
    print("FINAL COVERAGE")
    print("=" * 50)

    total_matches = min(len(completed_fixtures), 10)

    for label, available_count in coverage.items():
        percentage = (
            available_count / total_matches * 100
            if total_matches
            else 0
        )

        print(
            f"{label}: "
            f"{available_count}/{total_matches} "
            f"({percentage:.1f}%)"
        )


if __name__ == "__main__":
    main()