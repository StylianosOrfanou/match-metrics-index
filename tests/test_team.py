import pytest

from models.league import League
from models.team import Team


@pytest.fixture
def league():
    return League(
        name="Cyprus First Division",
        country="Cyprus",
        average_goals=2.65,
        home_advantage=1.06,
    )


def test_team_is_created_correctly(league):
    team = Team(
        name="Pafos",
        league=league,
        attack_rating=82,
        defence_rating=78,
        form_rating=80,
        home_strength=80,
        away_strength=75,
    )

    assert team.name == "Pafos"
    assert team.league == league
    assert team.attack_rating == 82
    assert team.defence_rating == 78
    assert team.form_rating == 80
    assert team.home_strength == 80
    assert team.away_strength == 75


def test_team_overall_rating_is_between_zero_and_one_hundred(
    league,
):
    team = Team(
        name="Pafos",
        league=league,
        attack_rating=82,
        defence_rating=78,
        form_rating=80,
        home_strength=80,
        away_strength=75,
    )

    assert 0 <= team.overall_rating <= 100


def test_team_rejects_empty_name(league):
    with pytest.raises(ValueError):
        Team(
            name="",
            league=league,
            attack_rating=82,
            defence_rating=78,
            form_rating=80,
            home_strength=80,
            away_strength=75,
        )


def test_team_rejects_rating_above_one_hundred(league):
    with pytest.raises(ValueError):
        Team(
            name="Pafos",
            league=league,
            attack_rating=120,
            defence_rating=78,
            form_rating=80,
            home_strength=80,
            away_strength=75,
        )


def test_team_rejects_negative_rating(league):
    with pytest.raises(ValueError):
        Team(
            name="Pafos",
            league=league,
            attack_rating=82,
            defence_rating=-10,
            form_rating=80,
            home_strength=80,
            away_strength=75,
        )


def test_team_rejects_invalid_home_strength(league):
    with pytest.raises(ValueError):
        Team(
            name="Pafos FC",
            league=league,
            attack_rating=82,
            defence_rating=80,
            form_rating=78,
            home_strength=101,
            away_strength=75,
        )


def test_team_rejects_invalid_away_strength(league):
    with pytest.raises(ValueError):
        Team(
            name="Pafos FC",
            league=league,
            attack_rating=82,
            defence_rating=80,
            form_rating=78,
            home_strength=80,
            away_strength=-1,
        )