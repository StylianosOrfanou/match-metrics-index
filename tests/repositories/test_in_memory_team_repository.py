import pytest

from repositories.in_memory_team_repository import (
    InMemoryTeamRepository,
)


def test_get_team_returns_existing_team():
    repository = InMemoryTeamRepository()

    team = repository.get_team("Aris Limassol")

    assert team.name == "Aris Limassol"
    assert team.attack_rating == 80
    assert team.defence_rating == 75
    assert team.form_rating == 85


def test_get_team_raises_error_for_unknown_team():
    repository = InMemoryTeamRepository()

    with pytest.raises(
        ValueError,
        match="Team 'Barcelona' was not found.",
    ):
        repository.get_team("Barcelona")