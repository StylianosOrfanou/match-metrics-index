from dataclasses import dataclass


@dataclass(frozen=True)
class EloUpdate:
    home_rating: float
    away_rating: float

    home_change: float
    away_change: float