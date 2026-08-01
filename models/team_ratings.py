from dataclasses import dataclass


@dataclass(frozen=True)
class TeamRatings:
    attack_rating: float
    defence_rating: float

    form_rating: float

    home_strength: float
    away_strength: float