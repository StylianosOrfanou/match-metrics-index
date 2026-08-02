from dataclasses import dataclass


@dataclass(frozen=True)
class TeamSignal:
    attack: float
    defence: float
    form: float
    home_strength: float
    away_strength: float
    weight: float