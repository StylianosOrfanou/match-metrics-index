from models.validation_match import (
    ValidationMatch,
)


def create_validation_match(
    home_goals: int = 2,
    away_goals: int = 1,
) -> ValidationMatch:
    return ValidationMatch(
        date="2026-07-26",
        competition="Cyprus First Division",
        home_team="Pafos FC",
        away_team="Omonia",
        home_goals=home_goals,
        away_goals=away_goals,
        bookmaker_home=0.40,
        bookmaker_draw=0.30,
        bookmaker_away=0.30,
    )