import pytest

from models.league import League


league = League(
    name="Cyprus First Division",
    country="Cyprus",
    average_goals=2.65,
    home_advantage=1.06,
)

from models.team import Team


def test_team_is_created_correctly():
    team = Team(
        name="Pafos",
        league=league,
        attack_rating=82,
        defence_rating=78,
        form_rating=80
    )

    assert team.name == "Pafos"
    assert team.attack_rating == 82
    assert team.defence_rating == 78
    assert team.form_rating == 80


def test_team_overall_rating_is_between_zero_and_one_hundred():
    team = Team(
        name="Pafos",
        league=league,
        attack_rating=82,
        defence_rating=78,
        form_rating=80
    )

    assert 0 <= team.overall_rating <= 100


def test_team_rejects_empty_name():
    with pytest.raises(ValueError):
        Team(
            name="",
            league=league,
            attack_rating=82,
            defence_rating=78,
            form_rating=80
        )


def test_team_rejects_rating_above_one_hundred():
    with pytest.raises(ValueError):
        Team(
            name="Pafos",
            league=league,
            attack_rating=120,
            defence_rating=78,
            form_rating=80
        )


def test_team_rejects_negative_rating():
    with pytest.raises(ValueError):
        Team(
            name="Pafos",
            league=league,
            attack_rating=82,
            defence_rating=-10,
            form_rating=80
        )