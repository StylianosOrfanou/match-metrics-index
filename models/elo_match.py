from dataclasses import dataclass


@dataclass(frozen=True)
class EloMatch:
    home_team: str
    away_team: str

    home_goals: int
    away_goals: int

    date: str