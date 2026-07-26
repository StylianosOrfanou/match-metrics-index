from config.settings import (
    MAX_EXPECTED_GOALS,
    MIN_EXPECTED_GOALS,
)
from models.league import League


def calculate_expected_goals(
    matchup_rating: float,
    league: League,
    is_home: bool = False,
) -> float:
    base_xg = league.average_goals / 2

    strength_multiplier = (
        matchup_rating / 50
    )

    expected_goals = (
        base_xg
        * strength_multiplier
    )

    if is_home:
        expected_goals *= (
            league.home_advantage
        )

    expected_goals = max(
        MIN_EXPECTED_GOALS,
        min(
            expected_goals,
            MAX_EXPECTED_GOALS,
        ),
    )

    return round(
        expected_goals,
        2,
    )