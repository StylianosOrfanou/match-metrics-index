from config.settings import (
    HOME_ADVANTAGE_XG,
    MAX_EXPECTED_GOALS,
    MIN_EXPECTED_GOALS
)


def calculate_expected_goals(
    matchup_rating: float,
    is_home: bool = False
) -> float:

    expected_goals = (
        MIN_EXPECTED_GOALS
        + (
            matchup_rating / 100
            * (
                MAX_EXPECTED_GOALS
                - MIN_EXPECTED_GOALS
            )
        )
    )

    if is_home:
        expected_goals += HOME_ADVANTAGE_XG

    expected_goals = max(
        MIN_EXPECTED_GOALS,
        min(expected_goals, MAX_EXPECTED_GOALS)
    )

    return round(expected_goals, 2)