from dataclasses import dataclass


@dataclass(frozen=True)
class BacktestReport:
    total_matches: int
    correct_predictions: int
    accuracy: float
    brier_score: float
    log_loss: float