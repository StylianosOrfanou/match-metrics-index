import math

import pytest

from validation.metrics import (
    three_way_log_loss,
)


def test_perfect_three_way_prediction():
    loss = three_way_log_loss(
        probabilities={
            "H": 1.0,
            "D": 0.0,
            "A": 0.0,
        },
        actual_result="H",
    )

    assert loss == pytest.approx(
        0.0,
        abs=1e-6,
    )


def test_uniform_three_way_prediction():
    loss = three_way_log_loss(
        probabilities={
            "H": 1 / 3,
            "D": 1 / 3,
            "A": 1 / 3,
        },
        actual_result="H",
    )

    assert loss == pytest.approx(
        math.log(3),
        abs=1e-6,
    )


def test_wrong_confident_prediction_is_penalized():
    loss = three_way_log_loss(
        probabilities={
            "H": 0.99,
            "D": 0.005,
            "A": 0.005,
        },
        actual_result="A",
    )

    assert loss > 5.0


def test_three_way_log_loss_rejects_invalid_result():
    with pytest.raises(ValueError):
        three_way_log_loss(
            probabilities={
                "H": 0.5,
                "D": 0.3,
                "A": 0.2,
            },
            actual_result="X",
        )


def test_three_way_log_loss_requires_all_results():
    with pytest.raises(ValueError):
        three_way_log_loss(
            probabilities={
                "H": 0.6,
                "A": 0.4,
            },
            actual_result="H",
        )


def test_three_way_log_loss_requires_sum_of_one():
    with pytest.raises(ValueError):
        three_way_log_loss(
            probabilities={
                "H": 0.6,
                "D": 0.3,
                "A": 0.3,
            },
            actual_result="H",
        )