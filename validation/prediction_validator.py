class PredictionValidator:

    VALID_RESULTS = {
        "H",
        "D",
        "A",
    }

    def accuracy(
        self,
        predictions: list[str],
        actual_results: list[str],
    ) -> float:
        if not predictions:
            raise ValueError(
                "Predictions cannot be empty."
            )

        if len(predictions) != len(
            actual_results
        ):
            raise ValueError(
                "Predictions and actual results "
                "must have the same length."
            )

        self._validate_results(
            predictions
        )

        self._validate_results(
            actual_results
        )

        correct_predictions = sum(
            prediction == actual
            for prediction, actual in zip(
                predictions,
                actual_results,
            )
        )

        return (
            correct_predictions
            / len(predictions)
        )

    @classmethod
    def _validate_results(
        cls,
        results: list[str],
    ) -> None:
        invalid_results = [
            result
            for result in results
            if result not in cls.VALID_RESULTS
        ]

        if invalid_results:
            raise ValueError(
                "Results must be H, D or A."
            )