import pytest

from models.league import League
from models.match import Match
from models.team import Team


league = League(
    name="Cyprus First Division",
    country="Cyprus",
    average_goals=2.65,
    home_advantage=1.06,
)


@pytest.fixture
def pafos():
    return Team(
        name="Pafos",
        league=league,
        attack_rating=82,
        defence_rating=78,
        form_rating=80,
        home_strength=84,
        away_strength=79,
    )


@pytest.fixture
def omonia():
    return Team(
        name="Omonia",
        league=league,
        attack_rating=75,
        defence_rating=80,
        form_rating=74,
        home_strength=80,
        away_strength=76,
    )


def test_match_is_created_correctly(
    pafos,
    omonia,
):
    match = Match(
        home_team=pafos,
        away_team=omonia,
    )

    assert match.home_team.name == "Pafos"
    assert match.away_team.name == "Omonia"


def test_match_rejects_invalid_home_team(
    omonia,
):
    with pytest.raises(TypeError):
        Match(
            home_team="Pafos",
            away_team=omonia,
        )


def test_match_rejects_invalid_away_team(
    pafos,
):
    with pytest.raises(TypeError):
        Match(
            home_team=pafos,
            away_team="Omonia",
        )


def test_team_cannot_play_against_itself(
    pafos,
):
    with pytest.raises(ValueError):
        Match(
            home_team=pafos,
            away_team=pafos,
        )