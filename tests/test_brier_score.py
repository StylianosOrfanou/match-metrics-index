import pytest

from validation.metrics import (
    brier_score,
)


def test_perfect_prediction():
    score = brier_score(
        predicted_probability=1.0,
        actual_outcome=1,
    )

    assert score == 0.0


def test_completely_wrong_prediction():
    score = brier_score(
        predicted_probability=1.0,
        actual_outcome=0,
    )

    assert score == 1.0


def test_fifty_percent_prediction():
    score = brier_score(
        predicted_probability=0.5,
        actual_outcome=1,
    )

    assert score == pytest.approx(
        0.25,
    )


def test_probability_must_be_valid():
    with pytest.raises(ValueError):
        brier_score(
            predicted_probability=1.5,
            actual_outcome=1,
        )


def test_outcome_must_be_binary():
    with pytest.raises(ValueError):
        brier_score(
            predicted_probability=0.5,
            actual_outcome=2,
        )