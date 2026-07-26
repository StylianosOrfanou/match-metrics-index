from models.validation_match import (
    ValidationMatch,
)


def test_home_result():
    match = ValidationMatch(
        date="2026-07-26",
        competition="Cyprus",

        home_team="Pafos FC",
        away_team="Omonia",

        home_goals=2,
        away_goals=1,

        bookmaker_home=0.40,
        bookmaker_draw=0.30,
        bookmaker_away=0.30,
    )

    assert match.result == "HOME"


def test_draw_result():
    match = ValidationMatch(
        date="2026-07-26",
        competition="Cyprus",

        home_team="Pafos FC",
        away_team="Omonia",

        home_goals=1,
        away_goals=1,

        bookmaker_home=0.40,
        bookmaker_draw=0.30,
        bookmaker_away=0.30,
    )

    assert match.result == "DRAW"


def test_away_result():
    match = ValidationMatch(
        date="2026-07-26",
        competition="Cyprus",

        home_team="Pafos FC",
        away_team="Omonia",

        home_goals=0,
        away_goals=2,

        bookmaker_home=0.40,
        bookmaker_draw=0.30,
        bookmaker_away=0.30,
    )

    assert match.result == "AWAY"