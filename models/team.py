from dataclasses import dataclass

from models.league import League


@dataclass(frozen=True)
class Team:
    name: str
    league: League
    attack_rating: float
    defence_rating: float
    form_rating: float
    home_strength: float
    away_strength: float

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Team name cannot be empty.")

        if not isinstance(self.league, League):
            raise TypeError("league must be a League object.")

        ratings = {
            "attack_rating": self.attack_rating,
            "defence_rating": self.defence_rating,
            "form_rating": self.form_rating,
            "home_strength": self.home_strength,
            "away_strength": self.away_strength,
        }

        for rating_name, rating_value in ratings.items():
            if not 0 <= rating_value <= 100:
                raise ValueError(
                    f"{rating_name} must be between 0 and 100."
                )

    @property
    def overall_rating(self) -> float:
        return round(
            (
                self.attack_rating
                + self.defence_rating
                + self.form_rating
            )
            / 3,
            2,
        )