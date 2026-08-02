from models.elo_match import EloMatch
from services.elo_builder_service import EloBuilderService


def test_new_teams_start_with_default_rating():

    matches = [
        EloMatch(
            home_team="A",
            away_team="B",
            home_goals=1,
            away_goals=0,
            date="2026-01-01",
        ),
    ]

    ratings = EloBuilderService().build(
        matches,
    )

    assert ratings["A"] > 1500
    assert ratings["B"] < 1500


def test_builder_returns_every_team():

    matches = [
        EloMatch(
            home_team="A",
            away_team="B",
            home_goals=1,
            away_goals=0,
            date="2026-01-01",
        ),
        EloMatch(
            home_team="C",
            away_team="A",
            home_goals=2,
            away_goals=2,
            date="2026-01-02",
        ),
    ]

    ratings = EloBuilderService().build(
        matches,
    )

    assert len(ratings) == 3