from dataclasses import dataclass


@dataclass
class HistoricalTeamState:
    name: str

    elo_rating: float = 1500.0

    matches: int = 0

    wins: int = 0
    draws: int = 0
    losses: int = 0

    goals_for: int = 0
    goals_against: int = 0