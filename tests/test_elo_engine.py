import pytest

from engines.elo_engine import EloEngine


def test_equal_ratings_produce_equal_probability():
    engine = EloEngine()

    probability = engine.expected_score(
        rating_a=1500,
        rating_b=1500,
    )

    assert probability == pytest.approx(
        0.5,
        abs=0.01,
    )


def test_higher_rating_produces_higher_probability():
    engine = EloEngine()

    stronger = engine.expected_score(
        rating_a=1700,
        rating_b=1500,
    )

    weaker = engine.expected_score(
        rating_a=1500,
        rating_b=1700,
    )

    assert stronger > weaker


def test_winner_gains_rating():
    engine = EloEngine()

    new_rating = engine.update_rating(
        rating=1500,
        expected_score=0.5,
        actual_score=1,
    )

    assert new_rating > 1500


def test_loser_loses_rating():
    engine = EloEngine()

    new_rating = engine.update_rating(
        rating=1500,
        expected_score=0.5,
        actual_score=0,
    )

    assert new_rating < 1500


def test_draw_changes_rating_slightly():
    engine = EloEngine()

    new_rating = engine.update_rating(
        rating=1500,
        expected_score=0.5,
        actual_score=0.5,
    )

    assert new_rating == pytest.approx(
        1500,
        abs=0.1,
    )


def test_higher_k_factor_changes_rating_more():
    low = EloEngine(k_factor=20)
    high = EloEngine(k_factor=40)

    low_rating = low.update_rating(
        rating=1500,
        expected_score=0.5,
        actual_score=1,
    )

    high_rating = high.update_rating(
        rating=1500,
        expected_score=0.5,
        actual_score=1,
    )

    assert (
        high_rating - 1500
        >
        low_rating - 1500
    )

def test_home_advantage_increases_home_expectation():
    engine = EloEngine(
        home_advantage=100,
    )

    neutral_probability = engine.expected_score(
        rating_a=1500,
        rating_b=1500,
    )

    home_probability = engine.expected_home_score(
        home_rating=1500,
        away_rating=1500,
    )

    assert home_probability > neutral_probability


def test_update_match_updates_both_teams():
    engine = EloEngine(
        home_advantage=0,
    )

    update = engine.update_match(
        home_rating=1500,
        away_rating=1500,
        home_goals=2,
        away_goals=0,
    )

    assert update.home_rating > 1500
    assert update.away_rating < 1500


def test_elo_changes_are_opposite():
    engine = EloEngine(
        home_advantage=0,
    )

    update = engine.update_match(
        home_rating=1500,
        away_rating=1500,
        home_goals=1,
        away_goals=0,
    )

    assert update.home_change == pytest.approx(
        -update.away_change,
        abs=0.01,
    )


def test_draw_against_equal_teams_keeps_ratings_equal():
    engine = EloEngine(
        home_advantage=0,
    )

    update = engine.update_match(
        home_rating=1500,
        away_rating=1500,
        home_goals=1,
        away_goals=1,
    )

    assert update.home_rating == pytest.approx(
        1500,
        abs=0.01,
    )

    assert update.away_rating == pytest.approx(
        1500,
        abs=0.01,
    )


def test_update_match_rejects_negative_goals():
    engine = EloEngine()

    with pytest.raises(ValueError):
        engine.update_match(
            home_rating=1500,
            away_rating=1500,
            home_goals=-1,
            away_goals=0,
        )