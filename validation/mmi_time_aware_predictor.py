from engines.prediction_engine import (
    PredictionEngine,
)
from services.match_service import (
    MatchService,
)
from validation.time_aware_predictor import (
    TimeAwarePredictor,
)


class MMITimeAwarePredictor(
    TimeAwarePredictor,
):

    def __init__(
        self,
        match_service: MatchService,
        prediction_engine: PredictionEngine,
    ) -> None:
        self._match_service = match_service
        self._prediction_engine = (
            prediction_engine
        )

    def predict(
        self,
        fixture: dict,
    ) -> dict[str, float]:
        home_team = fixture.get(
            "home_team"
        )

        away_team = fixture.get(
            "away_team"
        )

        if not home_team or not away_team:
            raise ValueError(
                "Fixture must contain home_team "
                "and away_team."
            )

        match = self._match_service.create_match(
            home_team_name=home_team,
            away_team_name=away_team,
        )

        prediction = (
            self._prediction_engine.predict(
                match
            )
        )

        probabilities = {
            "H": prediction.home_win / 100,
            "D": prediction.draw / 100,
            "A": prediction.away_win / 100,
        }

        total_probability = sum(
            probabilities.values()
        )

        if total_probability <= 0:
            raise ValueError(
                "Prediction probabilities "
                "must total more than zero."
            )

        # Protects the backtest metrics from tiny
        # rounding differences in 0–100 outputs.
        return {
            result: probability
            / total_probability
            for result, probability
            in probabilities.items()
        }

    def update(
        self,
        fixture: dict,
    ) -> None:
        # Historical state update will be added
        # after the mutable rating repository
        # is connected.
        return None