import pytest

from engines.recent_form_rating_builder import (
    RecentFormRatingBuilder,
)

from models.recent_form import RecentForm


def create_recent_forms() -> dict[str, RecentForm]:
    return {
        "Strong Team": RecentForm(
            matches=5,
            wins=4,
            draws=1,
            losses=0,
            goals_for=12,
            goals_against=3,
            home_matches=3,
            home_goals_for=8,
            home_goals_against=1,
            away_matches=2,
            away_goals_for=4,
            away_goals_against=2,
            expected_goals=0.0,
            shots=0,
        ),
        "Weak Team": RecentForm(
            matches=5,
            wins=0,
            draws=1,
            losses=4,
            goals_for=3,
            goals_against=12,
            home_matches=3,
            home_goals_for=2,
            home_goals_against=7,
            away_matches=2,
            away_goals_for=1,
            away_goals_against=5,
            expected_goals=0.0,
            shots=0,
        ),
    }


def test_builder_returns_ratings_for_every_team():
    ratings = RecentFormRatingBuilder().build(
        create_recent_forms()
    )

    assert len(ratings) == 2
    assert "Strong Team" in ratings
    assert "Weak Team" in ratings


def test_stronger_recent_attack_gets_higher_rating():
    ratings = RecentFormRatingBuilder().build(
        create_recent_forms()
    )

    assert (
        ratings["Strong Team"].attack_rating
        > ratings["Weak Team"].attack_rating
    )


def test_stronger_recent_defence_gets_higher_rating():
    ratings = RecentFormRatingBuilder().build(
        create_recent_forms()
    )

    assert (
        ratings["Strong Team"].defence_rating
        > ratings["Weak Team"].defence_rating
    )


def test_better_results_get_higher_form_rating():
    ratings = RecentFormRatingBuilder().build(
        create_recent_forms()
    )

    assert (
        ratings["Strong Team"].form_rating
        > ratings["Weak Team"].form_rating
    )


def test_stronger_home_performance_gets_higher_rating():
    ratings = RecentFormRatingBuilder().build(
        create_recent_forms()
    )

    assert (
        ratings["Strong Team"].home_strength
        > ratings["Weak Team"].home_strength
    )


def test_stronger_away_performance_gets_higher_rating():
    ratings = RecentFormRatingBuilder().build(
        create_recent_forms()
    )

    assert (
        ratings["Strong Team"].away_strength
        > ratings["Weak Team"].away_strength
    )


def test_builder_rejects_empty_input():
    with pytest.raises(ValueError):
        RecentFormRatingBuilder().build({})