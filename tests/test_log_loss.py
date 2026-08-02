import math
import pytest

from validation.metrics import (
    log_loss,
)


def test_perfect_prediction():
    assert log_loss(
        predicted_probability=1.0,
        actual_outcome=1,
    ) == pytest.approx(
        0.0,
        abs=1e-6,
    )


def test_half_probability():
    assert log_loss(
        predicted_probability=0.5,
        actual_outcome=1,
    ) == pytest.approx(
        math.log(2),
        abs=1e-6,
    )


def test_probability_zero_is_clipped():
    value = log_loss(
        predicted_probability=0.0,
        actual_outcome=1,
    )

    assert value > 0


def test_invalid_probability():
    with pytest.raises(ValueError):
        log_loss(
            predicted_probability=1.5,
            actual_outcome=1,
        )


def test_invalid_outcome():
    with pytest.raises(ValueError):
        log_loss(
            predicted_probability=0.5,
            actual_outcome=2,
        )