from dataclasses import dataclass

from validation.validation_result import (
    ValidationResult,
)


@dataclass(frozen=True)
class ValidationMetrics:
    results: list[ValidationResult]

    @property
    def total_matches(self) -> int:
        return len(self.results)

    @property
    def correct_predictions(self) -> int:
        return sum(
            result.winner_correct
            for result in self.results
        )

    @property
    def accuracy(self) -> float:
        if self.total_matches == 0:
            return 0.0

        return (
            self.correct_predictions
            / self.total_matches
        )