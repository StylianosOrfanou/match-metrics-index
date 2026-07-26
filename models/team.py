from dataclasses import dataclass

from models.league import League


@dataclass(frozen=True)
class Team:
    name: str
    league: League
    attack_rating: float
    defence_rating: float
    form_rating: float

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError(
                "Team name cannot be empty."
            )

        if not isinstance(self.league, League):
            raise TypeError(
                "league must be a League object."
            )

        ratings = (
            self.attack_rating,
            self.defence_rating,
            self.form_rating,
        )

        for rating in ratings:
            if rating < 0 or rating > 100:
                raise ValueError(
                    "Ratings must be between 0 and 100."
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