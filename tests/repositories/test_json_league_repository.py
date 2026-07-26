import json

import pytest

from repositories.json_league_repository import (
    JsonLeagueRepository,
)


def test_get_league_returns_existing_league(tmp_path):
    leagues_file = tmp_path / "leagues.json"

    leagues_data = [
        {
            "name": "Cyprus First Division",
            "country": "Cyprus",
            "average_goals": 2.65,
            "home_advantage": 1.06,
        }
    ]

    leagues_file.write_text(
        json.dumps(leagues_data),
        encoding="utf-8",
    )

    repository = JsonLeagueRepository(
        file_path=str(leagues_file)
    )

    league = repository.get_league(
        "Cyprus First Division"
    )

    assert league.name == "Cyprus First Division"
    assert league.country == "Cyprus"
    assert league.average_goals == 2.65
    assert league.home_advantage == 1.06


def test_get_league_raises_error_for_unknown_league(
    tmp_path,
):
    leagues_file = tmp_path / "leagues.json"

    leagues_file.write_text(
        "[]",
        encoding="utf-8",
    )

    repository = JsonLeagueRepository(
        file_path=str(leagues_file)
    )

    with pytest.raises(ValueError):
        repository.get_league("Unknown League")


def test_repository_raises_error_when_file_does_not_exist(
    tmp_path,
):
    missing_file = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        JsonLeagueRepository(
            file_path=str(missing_file)
        )


def test_repository_raises_error_for_invalid_json(
    tmp_path,
):
    leagues_file = tmp_path / "leagues.json"

    leagues_file.write_text(
        "{ invalid json }",
        encoding="utf-8",
    )

    with pytest.raises(json.JSONDecodeError):
        JsonLeagueRepository(
            file_path=str(leagues_file)
        )


def test_repository_raises_error_for_missing_league_field(
    tmp_path,
):
    leagues_file = tmp_path / "leagues.json"

    leagues_data = [
        {
            "name": "Cyprus First Division",
            "country": "Cyprus",
            "average_goals": 2.65,
        }
    ]

    leagues_file.write_text(
        json.dumps(leagues_data),
        encoding="utf-8",
    )

    with pytest.raises(KeyError):
        JsonLeagueRepository(
            file_path=str(leagues_file)
        )