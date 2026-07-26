from engines.prediction_engine import PredictionEngine
from models.prediction import Prediction
from models.validation_match import ValidationMatch
from services.match_service import MatchService
from validation.validation_result import ValidationResult


class Validator:

    def __init__(
        self,
        match_service: MatchService | None = None,
        prediction_engine: PredictionEngine | None = None,
    ) -> None:
        self._match_service = match_service
        self._prediction_engine = prediction_engine

    def validate_prediction(
        self,
        prediction: Prediction,
        actual_match: ValidationMatch,
    ) -> ValidationResult:
        return ValidationResult(
            prediction=prediction,
            actual_match=actual_match,
        )

    def validate_predictions(
        self,
        predictions: list[Prediction],
        matches: list[ValidationMatch],
    ) -> list[ValidationResult]:

        if len(predictions) != len(matches):
            raise ValueError(
                "Predictions and matches must have the same length."
            )

        return [
            self.validate_prediction(
                prediction,
                match,
            )
            for prediction, match in zip(
                predictions,
                matches,
            )
        ]

    def validate(
        self,
        matches: list[ValidationMatch],
    ) -> list[ValidationResult]:

        if (
            self._match_service is None
            or self._prediction_engine is None
        ):
            raise RuntimeError(
                "MatchService and PredictionEngine "
                "are required for automatic validation."
            )

        results = []

        for validation_match in matches:
            match = self._match_service.create_match(
                validation_match.home_team,
                validation_match.away_team,
            )

            prediction = self._prediction_engine.predict(
                match,
            )

            results.append(
                self.validate_prediction(
                    prediction,
                    validation_match,
                )
            )

        return results