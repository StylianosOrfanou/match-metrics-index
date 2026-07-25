from dataclasses import dataclass

from models.team_rating import calculate_team_rating


@dataclass
class Team:
    """
    Αντιπροσωπεύει μία ποδοσφαιρική ομάδα
    και τα βασικά ratings της.
    """

    name: str
    attack_rating: float
    defence_rating: float
    form_rating: float

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise ValueError("Team name must be text.")

        if not self.name.strip():
            raise ValueError("Team name cannot be empty.")

        ratings = {
            "attack_rating": self.attack_rating,
            "defence_rating": self.defence_rating,
            "form_rating": self.form_rating
        }

        for rating_name, rating_value in ratings.items():
            if not isinstance(rating_value, (int, float)):
                raise ValueError(
                    f"{rating_name} must be a number."
                )

            if rating_value < 0 or rating_value > 100:
                raise ValueError(
                    f"{rating_name} must be between 0 and 100."
                )

    @property
    def overall_rating(self):
        """
        Υπολογίζει αυτόματα το συνολικό Team Rating.
        """

        return calculate_team_rating(
            form_rating=self.form_rating,
            attack_rating=self.attack_rating,
            defence_rating=self.defence_rating
        )