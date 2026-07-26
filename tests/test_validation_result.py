from .helpers.prediction_factory import (
    create_prediction,
)

from .helpers.validation_match_factory import (
    create_validation_match,
)

from validation.validation_result import (
    ValidationResult,
)


def test_prediction_result_is_home():
    prediction = create_prediction(
        home_win=0.60,
        draw=0.25,
        away_win=0.15,
    )

    result = ValidationResult(
        prediction=prediction,
        actual_match=create_validation_match(),
    )

    assert result.predicted_result == "HOME"


def test_prediction_result_is_draw():
    prediction = create_prediction(
        home_win=0.30,
        draw=0.40,
        away_win=0.30,
    )

    result = ValidationResult(
        prediction=prediction,
        actual_match=create_validation_match(
            home_goals=1,
            away_goals=1,
        ),
    )

    assert result.predicted_result == "DRAW"


def test_prediction_result_is_away():
    prediction = create_prediction(
        home_win=0.20,
        draw=0.25,
        away_win=0.55,
    )

    result = ValidationResult(
        prediction=prediction,
        actual_match=create_validation_match(
            home_goals=0,
            away_goals=2,
        ),
    )

    assert result.predicted_result == "AWAY"


def test_winner_correct_is_true():
    prediction = create_prediction(
        home_win=0.60,
        draw=0.25,
        away_win=0.15,
    )

    result = ValidationResult(
        prediction=prediction,
        actual_match=create_validation_match(
            home_goals=2,
            away_goals=1,
        ),
    )

    assert result.winner_correct is True


def test_winner_correct_is_false():
    prediction = create_prediction(
        home_win=0.60,
        draw=0.25,
        away_win=0.15,
    )

    result = ValidationResult(
        prediction=prediction,
        actual_match=create_validation_match(
            home_goals=0,
            away_goals=1,
        ),
    )

    assert result.winner_correct is False