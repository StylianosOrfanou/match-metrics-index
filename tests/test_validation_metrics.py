from tests.helpers.prediction_factory import (
    create_prediction,
)

from tests.helpers.validation_match_factory import (
    create_validation_match,
)

from validation.validation_metrics import (
    ValidationMetrics,
)

from validation.validation_result import (
    ValidationResult,
)


def test_total_matches():
    results = [
        ValidationResult(
            prediction=create_prediction(),
            actual_match=create_validation_match(),
        ),
        ValidationResult(
            prediction=create_prediction(),
            actual_match=create_validation_match(),
        ),
    ]

    metrics = ValidationMetrics(results)

    assert metrics.total_matches == 2


def test_correct_predictions():
    results = [
        ValidationResult(
            prediction=create_prediction(
                home_win=0.6,
            ),
            actual_match=create_validation_match(
                home_goals=2,
                away_goals=1,
            ),
        ),
        ValidationResult(
            prediction=create_prediction(
                away_win=0.6,
                home_win=0.2,
            ),
            actual_match=create_validation_match(
                home_goals=0,
                away_goals=2,
            ),
        ),
    ]

    metrics = ValidationMetrics(results)

    assert metrics.correct_predictions == 2


def test_accuracy():
    results = [
        ValidationResult(
            prediction=create_prediction(
                home_win=0.6,
            ),
            actual_match=create_validation_match(
                home_goals=2,
                away_goals=1,
            ),
        ),
        ValidationResult(
            prediction=create_prediction(
                home_win=0.6,
            ),
            actual_match=create_validation_match(
                home_goals=0,
                away_goals=2,
            ),
        ),
    ]

    metrics = ValidationMetrics(results)

    assert metrics.accuracy == 0.5


def test_accuracy_empty_results():
    metrics = ValidationMetrics([])

    assert metrics.accuracy == 0.0