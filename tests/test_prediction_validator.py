from validation.prediction_validator import (
    PredictionValidator,
)


def test_correct_prediction_counts_as_hit():
    validator = PredictionValidator()

    accuracy = validator.accuracy(
        predictions=["H"],
        actual_results=["H"],
    )

    assert accuracy == 1.0


def test_wrong_prediction_counts_as_miss():
    validator = PredictionValidator()

    accuracy = validator.accuracy(
        predictions=["H"],
        actual_results=["A"],
    )

    assert accuracy == 0.0


def test_half_predictions():
    validator = PredictionValidator()

    accuracy = validator.accuracy(
        predictions=[
            "H",
            "A",
            "D",
            "H",
        ],
        actual_results=[
            "H",
            "D",
            "D",
            "A",
        ],
    )

    assert accuracy == 0.5


def test_empty_lists_are_rejected():
    validator = PredictionValidator()

    import pytest

    with pytest.raises(ValueError):
        validator.accuracy(
            [],
            [],
        )


def test_lengths_must_match():
    validator = PredictionValidator()

    import pytest

    with pytest.raises(ValueError):
        validator.accuracy(
            ["H"],
            [
                "H",
                "A",
            ],
        )