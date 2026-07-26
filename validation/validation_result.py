from dataclasses import dataclass

from models.prediction import Prediction
from models.validation_match import ValidationMatch


@dataclass(frozen=True)
class ValidationResult:
    """
    Represents the comparison between an MMI prediction
    and the actual result of a completed football match.
    """

    prediction: Prediction
    actual_match: ValidationMatch

    @property
    def predicted_result(self) -> str:
        if (
            self.prediction.home_win
            >= self.prediction.draw
            and self.prediction.home_win
            >= self.prediction.away_win
        ):
            return "HOME"

        if (
            self.prediction.away_win
            >= self.prediction.draw
            and self.prediction.away_win
            >= self.prediction.home_win
        ):
            return "AWAY"

        return "DRAW"

    @property
    def actual_result(self) -> str:
        return self.actual_match.result

    @property
    def winner_correct(self) -> bool:
        return (
            self.predicted_result
            == self.actual_result
        )