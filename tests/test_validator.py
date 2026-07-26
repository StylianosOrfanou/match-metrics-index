from tests.helpers.prediction_factory import (
    create_prediction,
)

from tests.helpers.validation_match_factory import (
    create_validation_match,
)

from validation.validator import (
    Validator,
)


def test_validate_prediction_returns_result():
    validator = Validator()

    prediction = create_prediction()

    actual_match = create_validation_match()

    result = validator.validate_prediction(
        prediction,
        actual_match,
    )

    assert result.prediction == prediction
    assert result.actual_match == actual_match


def test_validate_predictions_returns_results():
    validator = Validator()

    predictions = [
        create_prediction(),
        create_prediction(),
    ]

    matches = [
        create_validation_match(),
        create_validation_match(),
    ]

    results = validator.validate_predictions(
        predictions,
        matches,
    )

    assert len(results) == 2


def test_validate_predictions_checks_length():
    validator = Validator()

    predictions = [
        create_prediction(),
    ]

    matches = [
        create_validation_match(),
        create_validation_match(),
    ]

    import pytest

    with pytest.raises(ValueError):
        validator.validate_predictions(
            predictions,
            matches,
        )