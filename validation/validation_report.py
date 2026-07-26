from validation.validation_metrics import (
    ValidationMetrics,
)


class ValidationReport:

    def __init__(
        self,
        metrics: ValidationMetrics,
    ) -> None:
        self.metrics = metrics

    def generate(self) -> str:
        return (
            "\n"
            "MMI VALIDATION REPORT\n"
            + "-" * 40
            + "\n"
            f"Matches Tested: "
            f"{self.metrics.total_matches}\n"
            f"Correct Predictions: "
            f"{self.metrics.correct_predictions}\n"
            f"Accuracy: "
            f"{self.metrics.accuracy:.2%}"
        )

    def display(self) -> None:
        print(
            self.generate()
        )