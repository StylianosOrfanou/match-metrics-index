from builders.team_builder import TeamBuilder

from engines.rating_builder import (
    TeamSeasonStatistics,
)

from models.league import League


league = League(
    name="Cyprus First Division",
    country="Cyprus",
    average_goals=2.65,
    home_advantage=1.06,
)


def create_team(
    name: str,
) -> TeamSeasonStatistics:
    return TeamSeasonStatistics(
        name=name,
        goals_for_per_game=2.0,
        goals_against_per_game=1.0,
        home_goals_for_per_game=2.1,
        away_goals_for_per_game=1.9,
        home_goals_against_per_game=0.8,
        away_goals_against_per_game=1.2,
        shots_per_game=13,
        xg_per_game=1.8,
        wins=18,
        draws=6,
        losses=6,
    )


def test_builder_creates_team_objects():
    builder = TeamBuilder()

    teams = builder.build(
        [
            create_team("Pafos FC"),
            create_team("Omonia"),
        ],
        league,
    )

    assert len(teams) == 2

    assert teams[0].name == "Pafos FC"

    assert teams[1].name == "Omonia"


def test_generated_ratings_are_inside_limits():
    builder = TeamBuilder()

    team = builder.build(
        [
            create_team("Pafos FC"),
            create_team("Omonia"),
        ],
        league,
    )[0]

    assert 0 <= team.attack_rating <= 100
    assert 0 <= team.defence_rating <= 100
    assert 0 <= team.form_rating <= 100