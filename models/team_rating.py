from config.settings import (
    ATTACK_WEIGHT,
    DEFENCE_WEIGHT,
    FORM_WEIGHT
)


def calculate_team_rating(
    form_rating,
    attack_rating,
    defence_rating
):
    """
    Υπολογίζει το συνολικό Team Rating από 0 έως 100.
    """

    ratings = {
        "form_rating": form_rating,
        "attack_rating": attack_rating,
        "defence_rating": defence_rating
    }

    for name, rating in ratings.items():
        if not isinstance(rating, (int, float)):
            raise ValueError(f"{name} must be a number.")

        if rating < 0 or rating > 100:
            raise ValueError(
                f"{name} must be between 0 and 100."
            )

    team_rating = (
        attack_rating * ATTACK_WEIGHT
        + defence_rating * DEFENCE_WEIGHT
        + form_rating * FORM_WEIGHT
    )

    return round(team_rating, 2)