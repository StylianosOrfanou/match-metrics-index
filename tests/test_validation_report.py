from validation.validation_metrics import (
    ValidationMetrics,
)

from validation.validation_report import (
    ValidationReport,
)

from validation.validation_result import (
    ValidationResult,
)

from tests.helpers.prediction_factory import (
    create_prediction,
)

from tests.helpers.validation_match_factory import (
    create_validation_match,
)


def test_generate_report():
    results = [
        ValidationResult(
            prediction=create_prediction(
                home_win=0.60,
            ),
            actual_match=create_validation_match(
                home_goals=2,
                away_goals=1,
            ),
        ),
        ValidationResult(
            prediction=create_prediction(
                home_win=0.60,
            ),
            actual_match=create_validation_match(
                home_goals=0,
                away_goals=2,
            ),
        ),
    ]

    metrics = ValidationMetrics(results)

    report = ValidationReport(metrics)

    output = report.generate()

    assert "MMI VALIDATION REPORT" in output
    assert "Matches Tested: 2" in output
    assert "Correct Predictions: 1" in output
    assert "Accuracy: 50.00%" in output