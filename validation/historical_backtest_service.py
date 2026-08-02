from validation.backtest_report import (
    BacktestReport,
)
from validation.metrics import (
    three_way_brier_score,
    three_way_log_loss,
)
from validation.time_aware_predictor import (
    TimeAwarePredictor,
)


class HistoricalBacktestService:

    def __init__(
        self,
        predictor: TimeAwarePredictor,
    ) -> None:
        self._predictor = predictor

    def run(
        self,
        fixtures: list[dict],
    ) -> BacktestReport:
        if not fixtures:
            raise ValueError(
                "At least one fixture is required."
            )

        correct_predictions = 0
        brier_scores: list[float] = []
        log_losses: list[float] = []

        for fixture in fixtures:
            probabilities = (
                self._predictor.predict(
                    fixture
                )
            )

            actual_result = fixture[
                "actual_result"
            ]

            predicted_result = max(
                probabilities,
                key=probabilities.get,
            )

            if predicted_result == actual_result:
                correct_predictions += 1

            brier_scores.append(
                three_way_brier_score(
                    probabilities=probabilities,
                    actual_result=actual_result,
                )
            )

            log_losses.append(
                three_way_log_loss(
                    probabilities=probabilities,
                    actual_result=actual_result,
                )
            )

            # Critical: update only after prediction
            self._predictor.update(
                fixture
            )

        total_matches = len(fixtures)

        return BacktestReport(
            total_matches=total_matches,
            correct_predictions=correct_predictions,
            accuracy=round(
                correct_predictions
                / total_matches,
                6,
            ),
            brier_score=round(
                sum(brier_scores)
                / total_matches,
                6,
            ),
            log_loss=round(
                sum(log_losses)
                / total_matches,
                6,
            ),
        )