from scripts.download_historical_fixtures import (
    transform_fixture,
)


def test_transform_fixture():
    fixture = {
        "starting_at": "2025-09-15 18:00:00",
        "participants": [
            {
                "name": "Pafos FC",
                "meta": {
                    "location": "home",
                },
            },
            {
                "name": "Omonia Nicosia",
                "meta": {
                    "location": "away",
                },
            },
        ],
        "scores": [
            {
                "description": "CURRENT",
                "score": {
                    "participant": "home",
                    "goals": 2,
                },
            },
            {
                "description": "CURRENT",
                "score": {
                    "participant": "away",
                    "goals": 1,
                },
            },
        ],
    }

    result = transform_fixture(
        fixture
    )

    assert result == {
        "date": "2025-09-15 18:00:00",
        "home_team": "Pafos FC",
        "away_team": "Omonia",
        "home_goals": 2,
        "away_goals": 1,
        "actual_result": "H",
    }
