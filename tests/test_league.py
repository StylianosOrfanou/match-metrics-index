import pytest

from models.league import League


def test_league_is_created_correctly():
    league = League(
        name="Cyprus First Division",
        country="Cyprus",
        average_goals=2.65,
        home_advantage=1.06,
    )

    assert league.name == "Cyprus First Division"
    assert league.country == "Cyprus"
    assert league.average_goals == 2.65
    assert league.home_advantage == 1.06


def test_league_rejects_empty_name():
    with pytest.raises(ValueError):
        League(
            name="",
            country="Cyprus",
            average_goals=2.65,
            home_advantage=1.06,
        )


def test_league_rejects_empty_country():
    with pytest.raises(ValueError):
        League(
            name="Cyprus First Division",
            country="",
            average_goals=2.65,
            home_advantage=1.06,
        )


def test_league_rejects_invalid_average_goals():
    with pytest.raises(ValueError):
        League(
            name="Cyprus First Division",
            country="Cyprus",
            average_goals=0,
            home_advantage=1.06,
        )


def test_league_rejects_invalid_home_advantage():
    with pytest.raises(ValueError):
        League(
            name="Cyprus First Division",
            country="Cyprus",
            average_goals=2.65,
            home_advantage=0,
        )