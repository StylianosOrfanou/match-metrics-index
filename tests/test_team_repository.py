import pytest

from repositories.team_repository import TeamRepository


def test_team_repository_cannot_be_instantiated():
    with pytest.raises(TypeError):
        TeamRepository()