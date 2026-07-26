from dataclasses import dataclass


@dataclass(frozen=True)
class League:
    name: str
    country: str
    average_goals: float
    home_advantage: float

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError(
                "League name cannot be empty."
            )

        if not self.country.strip():
            raise ValueError(
                "Country cannot be empty."
            )

        if self.average_goals <= 0:
            raise ValueError(
                "Average goals must be greater than zero."
            )

        if self.home_advantage <= 0:
            raise ValueError(
                "Home advantage must be greater than zero."
            )