from engines.recent_form_rating_builder import (
    RecentFormRatings,
)
from models.team_ratings import TeamRatings
from services.team_signal_factory import (
    TeamSignalFactory,
)


def test_builds_signal_from_season():
    season = TeamRatings(
        attack_rating=80,
        defence_rating=70,
        form_rating=60,
        home_strength=75,
        away_strength=65,
    )

    signal = TeamSignalFactory().from_season(
        season,
        weight=0.6,
    )

    assert signal.attack == 80
    assert signal.defence == 70
    assert signal.form == 60
    assert signal.home_strength == 75
    assert signal.away_strength == 65
    assert signal.weight == 0.6


def test_builds_signal_from_recent():
    recent = RecentFormRatings(
        attack_rating=90,
        defence_rating=80,
        form_rating=70,
        home_strength=60,
        away_strength=50,
    )

    signal = TeamSignalFactory().from_recent(
        recent,
        weight=0.3,
    )

    assert signal.attack == 90
    assert signal.weight == 0.3


def test_builds_signal_from_elo():
    signal = TeamSignalFactory().from_elo(
        elo_rating=85,
        weight=0.1,
    )

    assert signal.attack == 85
    assert signal.defence == 85
    assert signal.form == 85
    assert signal.home_strength == 85
    assert signal.away_strength == 85
    assert signal.weight == 0.1