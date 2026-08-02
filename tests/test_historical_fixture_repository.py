from validation.historical_fixture_repository import (
    HistoricalFixtureRepository,
)


def test_repository_returns_fixtures():
    repository = HistoricalFixtureRepository()

    fixtures = repository.load()

    assert isinstance(fixtures, list)

import json


def test_repository_loads_json_file(tmp_path):
    filepath = (
        tmp_path
        / "fixtures.json"
    )

    filepath.write_text(
        json.dumps(
            [
                {
                    "home_team": "Pafos",
                    "away_team": "Omonia",
                    "actual_result": "H",
                },
            ]
        ),
        encoding="utf-8",
    )

    repository = HistoricalFixtureRepository(
        filepath=str(filepath),
    )

    fixtures = repository.load()

    assert len(fixtures) == 1
    assert (
        fixtures[0]["home_team"]
        == "Pafos"
    )