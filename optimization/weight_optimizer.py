from optimization.optimizer_result import (
    OptimizerResult,
)


class WeightOptimizer:

    def __init__(
        self,
        backtest_service,
    ) -> None:
        self._backtest_service = (
            backtest_service
        )

    def optimize(
        self,
        weight_sets:
        list[tuple[float, float, float]],
    ) -> OptimizerResult:
        if not weight_sets:
            raise ValueError(
                "At least one weight set is required."
            )

        results: list[OptimizerResult] = []

        for (
            season_weight,
            recent_weight,
            elo_weight,
        ) in weight_sets:
            self._validate_weights(
                season_weight=season_weight,
                recent_weight=recent_weight,
                elo_weight=elo_weight,
            )

            report = self._backtest_service.run(
                season_weight=season_weight,
                recent_weight=recent_weight,
                elo_weight=elo_weight,
            )

            results.append(
                OptimizerResult(
                    season_weight=season_weight,
                    recent_weight=recent_weight,
                    elo_weight=elo_weight,
                    report=report,
                )
            )

        return min(
            results,
            key=lambda result: (
                result.log_loss,
                result.brier_score,
                -result.accuracy,
            ),
        )

    @staticmethod
    def _validate_weights(
        season_weight: float,
        recent_weight: float,
        elo_weight: float,
    ) -> None:
        weights = (
            season_weight,
            recent_weight,
            elo_weight,
        )

        if any(
            weight < 0
            for weight in weights
        ):
            raise ValueError(
                "Weights cannot be negative."
            )

        if not round(
            sum(weights),
            10,
        ) == 1:
            raise ValueError(
                "Weights must total 1."
            )