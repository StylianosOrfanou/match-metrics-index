import pytest

from engines.rating_builder import (
    TeamSeasonStatistics,
)

from models.league import League
from models.recent_form import RecentForm

from services.rating_pipeline_service import (
    RatingPipelineService,
)

from models.team_ratings import TeamRatings
from engines.recent_form_rating_builder import (
    RecentFormRatings,
)
from services.team_signal_factory import (
    TeamSignalFactory,
)
from engines.weighted_rating_engine import (
    WeightedRatingEngine,
)


def test_weighted_engine_reproduces_pipeline():
    factory = TeamSignalFactory()

    season = TeamRatings(
        attack_rating=80,
        defence_rating=70,
        form_rating=60,
        home_strength=75,
        away_strength=65,
    )

    recent = RecentFormRatings(
        attack_rating=100,
        defence_rating=90,
        form_rating=80,
        home_strength=90,
        away_strength=70,
    )

    elo = 85

    result = WeightedRatingEngine().combine(
        [
            factory.from_season(
                season,
                0.6,
            ),
            factory.from_recent(
                recent,
                0.3,
            ),
            factory.from_elo(
                elo,
                0.1,
            ),
        ]
    )

    assert result.attack == pytest.approx(
        86.5,
    )

league = League(
    name="Cyprus First Division",
    country="Cyprus",
    average_goals=2.65,
    home_advantage=1.06,
)


def create_season_statistics(
    name: str,
    strong: bool,
) -> TeamSeasonStatistics:
    if strong:
        return TeamSeasonStatistics(
            name=name,
            goals_for_per_game=2.0,
            goals_against_per_game=0.8,
            home_goals_for_per_game=2.2,
            away_goals_for_per_game=1.8,
            home_goals_against_per_game=0.6,
            away_goals_against_per_game=1.0,
            shots_per_game=14.0,
            xg_per_game=1.8,
            wins=20,
            draws=5,
            losses=5,
        )

    return TeamSeasonStatistics(
        name=name,
        goals_for_per_game=0.8,
        goals_against_per_game=2.0,
        home_goals_for_per_game=1.0,
        away_goals_for_per_game=0.6,
        home_goals_against_per_game=1.8,
        away_goals_against_per_game=2.2,
        shots_per_game=7.0,
        xg_per_game=0.7,
        wins=4,
        draws=5,
        losses=21,
    )


def create_recent_form(
    strong: bool,
) -> RecentForm:
    if strong:
        return RecentForm(
            matches=5,
            wins=4,
            draws=1,
            losses=0,
            goals_for=11,
            goals_against=3,
            home_matches=3,
            home_goals_for=7,
            home_goals_against=1,
            away_matches=2,
            away_goals_for=4,
            away_goals_against=2,
            expected_goals=0.0,
            shots=0,
        )

    return RecentForm(
        matches=5,
        wins=0,
        draws=1,
        losses=4,
        goals_for=3,
        goals_against=11,
        home_matches=3,
        home_goals_for=2,
        home_goals_against=7,
        away_matches=2,
        away_goals_for=1,
        away_goals_against=4,
        expected_goals=0.0,
        shots=0,
    )


def test_pipeline_builds_team_for_every_statistics_entry():
    statistics = [
        create_season_statistics(
            "Strong Team",
            True,
        ),
        create_season_statistics(
            "Weak Team",
            False,
        ),
    ]

    recent_forms = {
        "Strong Team": create_recent_form(True),
        "Weak Team": create_recent_form(False),
    }

    teams = RatingPipelineService().build(
        season_statistics=statistics,
        recent_forms=recent_forms,
        league=league,
    )

    assert len(teams) == 2
    assert teams[0].name == "Strong Team"
    assert teams[1].name == "Weak Team"


def test_pipeline_preserves_stronger_team_advantage():
    statistics = [
        create_season_statistics(
            "Strong Team",
            True,
        ),
        create_season_statistics(
            "Weak Team",
            False,
        ),
    ]

    recent_forms = {
        "Strong Team": create_recent_form(True),
        "Weak Team": create_recent_form(False),
    }

    teams = RatingPipelineService().build(
        season_statistics=statistics,
        recent_forms=recent_forms,
        league=league,
    )

    strong_team = teams[0]
    weak_team = teams[1]

    assert (
        strong_team.attack_rating
        > weak_team.attack_rating
    )

    assert (
        strong_team.defence_rating
        > weak_team.defence_rating
    )

    assert (
        strong_team.form_rating
        > weak_team.form_rating
    )


def test_pipeline_uses_season_rating_when_recent_form_missing():
    statistics = [
        create_season_statistics(
            "Strong Team",
            True,
        ),
        create_season_statistics(
            "Weak Team",
            False,
        ),
    ]

    recent_forms = {
        "Strong Team": create_recent_form(True),
    }

    teams = RatingPipelineService().build(
        season_statistics=statistics,
        recent_forms=recent_forms,
        league=league,
    )

    assert len(teams) == 2


def test_pipeline_rejects_empty_statistics():
    with pytest.raises(ValueError):
        RatingPipelineService().build(
            season_statistics=[],
            recent_forms={
                "Team": create_recent_form(True),
            },
            league=league,
        )


def test_pipeline_rejects_empty_recent_forms():
    with pytest.raises(ValueError):
        RatingPipelineService().build(
            season_statistics=[
                create_season_statistics(
                    "Team",
                    True,
                )
            ],
            recent_forms={},
            league=league,
        )

def test_pipeline_uses_elo_rating():
    statistics = [
        create_season_statistics(
            "Strong Team",
            True,
        ),
        create_season_statistics(
            "Weak Team",
            False,
        ),
    ]

    recent_forms = {
        "Strong Team": create_recent_form(True),
        "Weak Team": create_recent_form(False),
    }

    without_elo = RatingPipelineService().build(
        season_statistics=statistics,
        recent_forms=recent_forms,
        league=league,
    )

    with_elo = RatingPipelineService().build(
        season_statistics=statistics,
        recent_forms=recent_forms,
        league=league,
        elo_ratings={
            "Strong Team": 20.0,
            "Weak Team": 95.0,
        },
    )

    assert (
        with_elo[0].attack_rating
        < without_elo[0].attack_rating
    )

    assert (
        with_elo[1].attack_rating
        > without_elo[1].attack_rating
    )