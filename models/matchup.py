from config.settings import (
    MATCHUP_ATTACK_WEIGHT,
    MATCHUP_DEFENCE_WEAKNESS_WEIGHT
)


def calculate_matchup_rating(
    team_attack,
    opponent_defence
):
    """
    Υπολογίζει πόσο ευνοϊκό είναι ένα επιθετικό matchup.
    """

    values = {
        "team_attack": team_attack,
        "opponent_defence": opponent_defence
    }

    for name, value in values.items():
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number.")

        if value < 0 or value > 100:
            raise ValueError(
                f"{name} must be between 0 and 100."
            )

    opponent_defensive_weakness = 100 - opponent_defence

    matchup_rating = (
        team_attack * MATCHUP_ATTACK_WEIGHT
        + opponent_defensive_weakness
        * MATCHUP_DEFENCE_WEAKNESS_WEIGHT
    )

    return round(matchup_rating, 2)