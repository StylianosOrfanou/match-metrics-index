import json
from pathlib import Path
from typing import Any

from clients.sportmonks_client import (
    SportmonksClient,
)
from repositories.sportmonks_elo_repository import (
    TEAM_NAME_MAPPING,
)


CYPRUS_SEASON_ID = 25996
OUTPUT_PATH = Path(
    "data/historical_fixtures.json"
)


def transform_fixture(
    fixture: dict[str, Any],
) -> dict[str, Any] | None:
    home_team = _get_team_name(
        fixture=fixture,
        location="home",
    )

    away_team = _get_team_name(
        fixture=fixture,
        location="away",
    )

    home_goals = _get_score(
        fixture=fixture,
        participant="home",
    )

    away_goals = _get_score(
        fixture=fixture,
        participant="away",
    )

    date = fixture.get(
        "starting_at"
    )

    if (
        home_team is None
        or away_team is None
        or home_goals is None
        or away_goals is None
        or date is None
    ):
        return None

    if home_goals > away_goals:
        actual_result = "H"
    elif home_goals < away_goals:
        actual_result = "A"
    else:
        actual_result = "D"

    return {
        "date": date,
        "home_team": home_team,
        "away_team": away_team,
        "home_goals": home_goals,
        "away_goals": away_goals,
        "actual_result": actual_result,
    }


def download_historical_fixtures(
    season_id: int = CYPRUS_SEASON_ID,
    output_path: Path = OUTPUT_PATH,
    client: SportmonksClient | None = None,
) -> list[dict[str, Any]]:
    sportmonks_client = (
        client
        or SportmonksClient()
    )

    response = sportmonks_client.get(
        f"seasons/{season_id}",
        params={
            "include": (
                "fixtures.participants;"
                "fixtures.scores"
            ),
        },
    )

    season = response.get(
        "data",
        {},
    )

    raw_fixtures = season.get(
        "fixtures",
        [],
    )

    fixtures: list[dict[str, Any]] = []

    skipped = 0

    for raw_fixture in raw_fixtures:
        fixture = transform_fixture(
            raw_fixture
        )

        if fixture is None:
            skipped += 1
            continue

        fixtures.append(
            fixture
        )

    fixtures.sort(
        key=lambda fixture: fixture["date"]
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            fixtures,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print()
    print("MMI HISTORICAL FIXTURE DOWNLOAD")
    print("-" * 60)
    print(
        f"Season: {season_id}"
    )
    print(
        f"Raw fixtures: {len(raw_fixtures)}"
    )
    print(
        f"Completed fixtures: {len(fixtures)}"
    )
    print(
        f"Skipped fixtures: {skipped}"
    )
    print(
        f"Output: {output_path}"
    )
    print("-" * 60)

    return fixtures


def _get_team_name(
    fixture: dict,
    location: str,
) -> str | None:
    participants = fixture.get(
        "participants",
        [],
    )

    for participant in participants:
        meta = participant.get(
            "meta",
            {},
        )

        if meta.get("location") != location:
            continue

        name = participant.get(
            "name"
        )

        if name is None:
            return None

        return TEAM_NAME_MAPPING.get(
            name,
            name,
        )

    return None


def _get_score(
    fixture: dict,
    participant: str,
) -> int | None:
    scores = fixture.get(
        "scores",
        [],
    )

    for score in scores:
        if score.get(
            "description"
        ) != "CURRENT":
            continue

        score_data = score.get(
            "score",
            {},
        )

        if (
            score_data.get("participant")
            == participant
        ):
            return score_data.get(
                "goals"
            )

    return None


def main() -> None:
    download_historical_fixtures()


if __name__ == "__main__":
    main()