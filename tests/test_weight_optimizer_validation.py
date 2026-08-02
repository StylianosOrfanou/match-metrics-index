import pytest

from optimization.weight_optimizer import (
    WeightOptimizer,
)
from validation.backtest_report import (
    BacktestReport,
)


class FakeBacktestService:

    def run(
        self,
        season_weight,
        recent_weight,
        elo_weight,
    ):
        return BacktestReport(
            total_matches=100,
            correct_predictions=60,
            accuracy=0.60,
            brier_score=0.20,
            log_loss=0.80,
        )


def test_empty_weight_sets_raise_error():
    optimizer = WeightOptimizer(
        FakeBacktestService(),
    )

    with pytest.raises(ValueError):
        optimizer.optimize([])


def test_negative_weight_raises_error():
    optimizer = WeightOptimizer(
        FakeBacktestService(),
    )

    with pytest.raises(ValueError):
        optimizer.optimize(
            [
                (-0.1, 0.8, 0.3),
            ]
        )


def test_weights_must_sum_to_one():
    optimizer = WeightOptimizer(
        FakeBacktestService(),
    )

    with pytest.raises(ValueError):
        optimizer.optimize(
            [
                (0.5, 0.5, 0.5),
            ]
        )