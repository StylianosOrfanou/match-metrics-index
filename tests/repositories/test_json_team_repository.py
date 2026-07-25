import json

import pytest

from repositories.json_team_repository import JsonTeamRepository


def test_get_team_returns_existing_team(tmp_path):
    teams_file = tmp_path / "teams.json"

    teams_data = [
        {
            "name": "Pafos FC",
            "attack_rating": 82,
            "defence_rating": 80,
            "form_rating": 78,
        }
    ]

    teams_file.write_text(
        json.dumps(teams_data),
        encoding="utf-8",
    )

    repository = JsonTeamRepository(
        file_path=str(teams_file)
    )

    team = repository.get_team("Pafos FC")

    assert team.name == "Pafos FC"
    assert team.attack_rating == 82
    assert team.defence_rating == 80
    assert team.form_rating == 78


def test_get_team_raises_error_for_unknown_team(tmp_path):
    teams_file = tmp_path / "teams.json"

    teams_file.write_text(
        "[]",
        encoding="utf-8",
    )

    repository = JsonTeamRepository(
        file_path=str(teams_file)
    )

    with pytest.raises(ValueError):
        repository.get_team("Unknown Team")


def test_repository_raises_error_when_file_does_not_exist(
    tmp_path,
):
    missing_file = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        JsonTeamRepository(
            file_path=str(missing_file)
        )
def test_repository_raises_error_for_invalid_json(tmp_path):
    teams_file = tmp_path / "teams.json"

    teams_file.write_text(
        "{ invalid json }",
        encoding="utf-8",
    )

    with pytest.raises(json.JSONDecodeError):
        JsonTeamRepository(
            file_path=str(teams_file)
        )


def test_repository_raises_error_for_missing_team_field(tmp_path):
    teams_file = tmp_path / "teams.json"

    teams_data = [
        {
            "name": "Pafos FC",
            "attack_rating": 82,
            "defence_rating": 80,
        }
    ]

    teams_file.write_text(
        json.dumps(teams_data),
        encoding="utf-8",
    )

    with pytest.raises(KeyError):
        JsonTeamRepository(
            file_path=str(teams_file)
        )