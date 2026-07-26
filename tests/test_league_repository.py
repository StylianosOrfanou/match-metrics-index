import pytest

from repositories.league_repository import LeagueRepository


def test_league_repository_cannot_be_instantiated():
    with pytest.raises(TypeError):
        LeagueRepository()