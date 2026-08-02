import pytest

from engines.elo_rating_normalizer import (
    EloRatingNormalizer,
)


def test_highest_elo_receives_maximum_rating():
    ratings = {
        "Strong Team": 1700,
        "Average Team": 1500,
        "Weak Team": 1300,
    }

    normalized = EloRatingNormalizer().normalize(
        ratings
    )

    assert normalized["Strong Team"] == 95.0


def test_lowest_elo_receives_minimum_rating():
    ratings = {
        "Strong Team": 1700,
        "Average Team": 1500,
        "Weak Team": 1300,
    }

    normalized = EloRatingNormalizer().normalize(
        ratings
    )

    assert normalized["Weak Team"] == 20.0


def test_middle_elo_receives_middle_rating():
    ratings = {
        "Strong Team": 1700,
        "Average Team": 1500,
        "Weak Team": 1300,
    }

    normalized = EloRatingNormalizer().normalize(
        ratings
    )

    assert normalized["Average Team"] == pytest.approx(
        57.5,
        abs=0.01,
    )


def test_equal_elos_receive_midpoint_rating():
    ratings = {
        "Team A": 1500,
        "Team B": 1500,
    }

    normalized = EloRatingNormalizer().normalize(
        ratings
    )

    assert normalized["Team A"] == 57.5
    assert normalized["Team B"] == 57.5


def test_normalizer_rejects_empty_input():
    with pytest.raises(ValueError):
        EloRatingNormalizer().normalize({})


def test_normalizer_rejects_invalid_range():
    with pytest.raises(ValueError):
        EloRatingNormalizer(
            minimum_rating=95,
            maximum_rating=20,
        )