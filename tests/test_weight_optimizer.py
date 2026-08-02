from optimization.weight_optimizer import (
    WeightOptimizer,
)
from validation.backtest_report import (
    BacktestReport,
)


class FakeBacktestService:

    def __init__(self):
        self.calls = []

    def run(
        self,
        season_weight,
        recent_weight,
        elo_weight,
    ):
        self.calls.append(
            (
                season_weight,
                recent_weight,
                elo_weight,
            )
        )

        return BacktestReport(
            total_matches=240,
            correct_predictions=145,
            accuracy=0.604,
            brier_score=0.198,
            log_loss=0.812,
        )


def test_optimizer_returns_best_result():
    optimizer = WeightOptimizer(
        FakeBacktestService(),
    )

    result = optimizer.optimize(
        weight_sets=[
            (0.6, 0.3, 0.1),
        ],
    )

    assert result.accuracy == 0.604