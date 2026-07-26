import json

import pytest

from repositories.json_validation_repository import (
    JsonValidationRepository,
)


def test_repository_loads_validation_matches(
    tmp_path,
):
    file_path = tmp_path / "validation_matches.json"

    data = [
        {
            "date": "2026-07-26",
            "competition": "Cyprus",
            "home_team": "Pafos FC",
            "away_team": "Omonia",
            "home_goals": 2,
            "away_goals": 1,
            "bookmaker_home": 0.40,
            "bookmaker_draw": 0.30,
            "bookmaker_away": 0.30,
        }
    ]

    file_path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    repository = JsonValidationRepository(
        file_path=str(file_path),
    )

    matches = repository.get_all()

    assert len(matches) == 1

    match = matches[0]

    assert match.home_team == "Pafos FC"
    assert match.away_team == "Omonia"
    assert match.home_goals == 2
    assert match.away_goals == 1
    assert match.result == "HOME"


def test_repository_returns_all_matches(
    tmp_path,
):
    file_path = tmp_path / "validation_matches.json"

    data = [
        {
            "date": "2026-07-25",
            "competition": "Cyprus",
            "home_team": "Pafos FC",
            "away_team": "Omonia",
            "home_goals": 1,
            "away_goals": 0,
            "bookmaker_home": 0.40,
            "bookmaker_draw": 0.30,
            "bookmaker_away": 0.30,
        },
        {
            "date": "2026-07-26",
            "competition": "Cyprus",
            "home_team": "Omonia",
            "away_team": "Pafos FC",
            "home_goals": 1,
            "away_goals": 1,
            "bookmaker_home": 0.40,
            "bookmaker_draw": 0.30,
            "bookmaker_away": 0.30,
        },
    ]

    file_path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    repository = JsonValidationRepository(
        file_path=str(file_path),
    )

    matches = repository.get_all()

    assert len(matches) == 2
    assert matches[0].result == "HOME"
    assert matches[1].result == "DRAW"


def test_repository_raises_error_when_file_missing(
    tmp_path,
):
    file_path = tmp_path / "missing.json"

    repository = JsonValidationRepository(
        file_path=str(file_path),
    )

    with pytest.raises(FileNotFoundError):
        repository.get_all()


def test_repository_rejects_non_list_json(
    tmp_path,
):
    file_path = tmp_path / "validation_matches.json"

    file_path.write_text(
        json.dumps(
            {
                "home_team": "Pafos FC",
            }
        ),
        encoding="utf-8",
    )

    repository = JsonValidationRepository(
        file_path=str(file_path),
    )

    with pytest.raises(
        ValueError,
        match="JSON list",
    ):
        repository.get_all()