import pytest

from engines.rating_normalizer import (
    RatingNormalizer,
)


def test_highest_value_receives_maximum_rating():
    normalizer = RatingNormalizer()

    result = normalizer.normalize_value(
        value=100,
        values=[
            0,
            50,
            100,
        ],
    )

    assert result == 95.0


def test_lowest_value_receives_minimum_rating():
    normalizer = RatingNormalizer()

    result = normalizer.normalize_value(
        value=0,
        values=[
            0,
            50,
            100,
        ],
    )

    assert result == 20.0


def test_middle_value_receives_midpoint():
    normalizer = RatingNormalizer()

    result = normalizer.normalize_value(
        value=50,
        values=[
            0,
            50,
            100,
        ],
    )

    assert result == pytest.approx(
        57.5,
    )


def test_reverse_normalization():
    normalizer = RatingNormalizer()

    result = normalizer.normalize_value(
        value=0,
        values=[
            0,
            50,
            100,
        ],
        reverse=True,
    )

    assert result == 95.0


def test_equal_values_receive_midpoint():
    normalizer = RatingNormalizer()

    result = normalizer.normalize_value(
        value=10,
        values=[
            10,
            10,
        ],
    )

    assert result == 57.5


def test_empty_values_are_rejected():
    normalizer = RatingNormalizer()

    with pytest.raises(ValueError):
        normalizer.normalize_value(
            value=10,
            values=[],
        )