import pytest

from engines.historical_rating_builder import (
    HistoricalRatingBuilder,
)
from models.historical_team_state import (
    HistoricalTeamState,
)
from models.league import League
from models.team import Team

def test_builder_returns_ratings_for_every_team():
    states = {
        "Strong Team": HistoricalTeamState(
            name="Strong Team",
            matches=5,
            wins=4,
            draws=1,
            losses=0,
            goals_for=12,
            goals_against=3,
            home_matches=3,
            home_goals_for=8,
            home_goals_against=2,
            away_matches=2,
            away_goals_for=4,
            away_goals_against=1,
        ),
        "Weak Team": HistoricalTeamState(
            name="Weak Team",
            matches=5,
            wins=0,
            draws=1,
            losses=4,
            goals_for=3,
            goals_against=12,
            home_matches=2,
            home_goals_for=1,
            home_goals_against=5,
            away_matches=3,
            away_goals_for=2,
            away_goals_against=7,
        ),
    }

    ratings = HistoricalRatingBuilder().build(
        states
    )

    assert set(ratings) == {
        "Strong Team",
        "Weak Team",
    }


def test_stronger_attack_receives_higher_rating():
    states = _create_states()

    ratings = HistoricalRatingBuilder().build(
        states
    )

    assert (
        ratings["Strong Team"].attack_rating
        > ratings["Weak Team"].attack_rating
    )


def test_stronger_defence_receives_higher_rating():
    states = _create_states()

    ratings = HistoricalRatingBuilder().build(
        states
    )

    assert (
        ratings["Strong Team"].defence_rating
        > ratings["Weak Team"].defence_rating
    )


def test_better_results_receive_higher_form_rating():
    states = _create_states()

    ratings = HistoricalRatingBuilder().build(
        states
    )

    assert (
        ratings["Strong Team"].form_rating
        > ratings["Weak Team"].form_rating
    )


def test_home_and_away_strength_are_calculated():
    ratings = HistoricalRatingBuilder().build(
        _create_states()
    )

    assert (
        ratings["Strong Team"].home_strength
        > ratings["Weak Team"].home_strength
    )

    assert (
        ratings["Strong Team"].away_strength
        > ratings["Weak Team"].away_strength
    )


def test_empty_states_are_rejected():
    with pytest.raises(ValueError):
        HistoricalRatingBuilder().build({})


def _create_states():
    return {
        "Strong Team": HistoricalTeamState(
            name="Strong Team",
            matches=5,
            wins=4,
            draws=1,
            losses=0,
            goals_for=12,
            goals_against=3,
            home_matches=3,
            home_goals_for=8,
            home_goals_against=2,
            away_matches=2,
            away_goals_for=4,
            away_goals_against=1,
        ),
        "Weak Team": HistoricalTeamState(
            name="Weak Team",
            matches=5,
            wins=0,
            draws=1,
            losses=4,
            goals_for=3,
            goals_against=12,
            home_matches=2,
            home_goals_for=1,
            home_goals_against=5,
            away_matches=3,
            away_goals_for=2,
            away_goals_against=7,
        ),
    }


def test_builder_can_build_team_objects():
    league = League(
        name="Cyprus",
        country="Cyprus",
        average_goals=2.65,
        home_advantage=1.06,
    )

    builder = HistoricalRatingBuilder()

    teams = builder.build_teams(
        states=_create_states(),
        league=league,
    )

    assert isinstance(
        teams["Strong Team"],
        Team,
    )

    assert (
        teams["Strong Team"].name
        == "Strong Team"
    )

    assert (
        teams["Strong Team"].league
        is league
    )