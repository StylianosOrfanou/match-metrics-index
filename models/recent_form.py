from dataclasses import dataclass


@dataclass(frozen=True)
class RecentForm:
    matches: int

    wins: int
    draws: int
    losses: int

    goals_for: int
    goals_against: int

    home_matches: int
    home_goals_for: int
    home_goals_against: int

    away_matches: int
    away_goals_for: int
    away_goals_against: int

    expected_goals: float
    shots: int