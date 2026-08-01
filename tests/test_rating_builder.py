import pytest

from engines.rating_builder import (
    RatingBuilder,
    TeamSeasonStatistics,
)


def create_team(
    name: str,
    goals_for: float,
    goals_against: float,
    home_goals_for: float,
    away_goals_for: float,
    home_goals_against: float,
    away_goals_against: float,
    shots: float,
    xg: float,
    wins: int,
    draws: int,
    losses: int,
) -> TeamSeasonStatistics:
    return TeamSeasonStatistics(
        name=name,
        goals_for_per_game=goals_for,
        goals_against_per_game=goals_against,
        home_goals_for_per_game=home_goals_for,
        away_goals_for_per_game=away_goals_for,
        home_goals_against_per_game=home_goals_against,
        away_goals_against_per_game=away_goals_against,
        shots_per_game=shots,
        xg_per_game=xg,
        wins=wins,
        draws=draws,
        losses=losses,
    )


@pytest.fixture
def teams():
    return [
        create_team(
            name="Strong Team",
            goals_for=2.2,
            goals_against=0.7,
            home_goals_for=2.5,
            away_goals_for=1.9,
            home_goals_against=0.5,
            away_goals_against=0.9,
            shots=15.0,
            xg=1.9,
            wins=20,
            draws=5,
            losses=3,
        ),
        create_team(
            name="Average Team",
            goals_for=1.4,
            goals_against=1.3,
            home_goals_for=1.6,
            away_goals_for=1.2,
            home_goals_against=1.1,
            away_goals_against=1.5,
            shots=11.0,
            xg=1.3,
            wins=10,
            draws=8,
            losses=10,
        ),
        create_team(
            name="Weak Team",
            goals_for=0.6,
            goals_against=2.1,
            home_goals_for=0.8,
            away_goals_for=0.4,
            home_goals_against=1.8,
            away_goals_against=2.4,
            shots=7.0,
            xg=0.7,
            wins=3,
            draws=4,
            losses=21,
        ),
    ]


def test_builder_returns_rating_for_every_team(
    teams,
):
    ratings = RatingBuilder().build(teams)

    assert len(ratings) == 3
    assert "Strong Team" in ratings
    assert "Weak Team" in ratings


def test_stronger_attack_receives_higher_rating(
    teams,
):
    ratings = RatingBuilder().build(teams)

    assert (
        ratings["Strong Team"].attack_rating
        > ratings["Weak Team"].attack_rating
    )


def test_better_defence_receives_higher_rating(
    teams,
):
    ratings = RatingBuilder().build(teams)

    assert (
        ratings["Strong Team"].defence_rating
        > ratings["Weak Team"].defence_rating
    )


def test_better_results_produce_higher_form(
    teams,
):
    ratings = RatingBuilder().build(teams)

    assert (
        ratings["Strong Team"].form_rating
        > ratings["Weak Team"].form_rating
    )


def test_all_ratings_stay_between_zero_and_one_hundred(
    teams,
):
    ratings = RatingBuilder().build(teams)

    for team_ratings in ratings.values():
        assert 0 <= team_ratings.attack_rating <= 100
        assert 0 <= team_ratings.defence_rating <= 100
        assert 0 <= team_ratings.form_rating <= 100
        assert 0 <= team_ratings.home_strength <= 100
        assert 0 <= team_ratings.away_strength <= 100


def test_builder_rejects_empty_team_list():
    with pytest.raises(ValueError):
        RatingBuilder().build([])