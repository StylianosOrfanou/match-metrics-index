import pytest

from engines.weighted_rating_engine import (
    WeightedRatingEngine,
)
from models.team_signal import TeamSignal


def test_single_signal_returns_same_values():
    signal = TeamSignal(
        attack=80,
        defence=70,
        form=60,
        home_strength=75,
        away_strength=65,
        weight=1.0,
    )

    result = WeightedRatingEngine().combine(
        [signal],
    )

    assert result.attack == 80
    assert result.defence == 70
    assert result.form == 60
    assert result.home_strength == 75
    assert result.away_strength == 65


def test_two_signals_are_weighted_correctly():
    season = TeamSignal(
        attack=80,
        defence=70,
        form=60,
        home_strength=75,
        away_strength=65,
        weight=0.8,
    )

    elo = TeamSignal(
        attack=60,
        defence=90,
        form=80,
        home_strength=60,
        away_strength=70,
        weight=0.2,
    )

    result = WeightedRatingEngine().combine(
        [
            season,
            elo,
        ],
    )

    assert result.attack == pytest.approx(
        76.0,
    )

    assert result.defence == pytest.approx(
        74.0,
    )


def test_empty_signal_list_is_rejected():
    with pytest.raises(ValueError):
        WeightedRatingEngine().combine([])