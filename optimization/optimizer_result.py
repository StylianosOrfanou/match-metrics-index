from dataclasses import dataclass

from validation.backtest_report import (
    BacktestReport,
)


@dataclass(frozen=True)
class OptimizerResult:
    season_weight: float
    recent_weight: float
    elo_weight: float
    report: BacktestReport

    @property
    def accuracy(self) -> float:
        return self.report.accuracy

    @property
    def brier_score(self) -> float:
        return self.report.brier_score

    @property
    def log_loss(self) -> float:
        return self.report.log_loss