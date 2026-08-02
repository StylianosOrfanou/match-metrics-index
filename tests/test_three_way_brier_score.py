import pytest

from validation.metrics import (
    three_way_brier_score,
)


def test_perfect_prediction():
    score = three_way_brier_score(
        probabilities={
            "H": 1.0,
            "D": 0.0,
            "A": 0.0,
        },
        actual_result="H",
    )

    assert score == 0.0


def test_uniform_prediction():
    score = three_way_brier_score(
        probabilities={
            "H": 1 / 3,
            "D": 1 / 3,
            "A": 1 / 3,
        },
        actual_result="H",
    )

    assert score == pytest.approx(
        2 / 3,
        abs=1e-6,
    )


def test_invalid_result():
    with pytest.raises(ValueError):
        three_way_brier_score(
            probabilities={
                "H": 0.5,
                "D": 0.3,
                "A": 0.2,
            },
            actual_result="X",
        )


def test_probabilities_must_sum_to_one():
    with pytest.raises(ValueError):
        three_way_brier_score(
            probabilities={
                "H": 0.5,
                "D": 0.5,
                "A": 0.5,
            },
            actual_result="H",
        )