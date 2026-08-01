from engines.rating_fusion_engine import (
    RatingFusionEngine,
)

from engines.recent_form_rating_builder import (
    RecentFormRatings,
)

from models.team_ratings import TeamRatings


def test_attack_is_weighted_correctly():

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
        home_strength=85,
        away_strength=75,
    )

    fused = RatingFusionEngine().fuse(
        season,
        recent,
    )

    assert fused.attack_rating == 85


def test_form_is_weighted_correctly():

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
        home_strength=85,
        away_strength=75,
    )

    fused = RatingFusionEngine().fuse(
        season,
        recent,
    )

    assert fused.form_rating == 70


def test_fused_values_remain_inside_limits():

    season = TeamRatings(
        attack_rating=95,
        defence_rating=95,
        form_rating=95,
        home_strength=95,
        away_strength=95,
    )

    recent = RecentFormRatings(
        attack_rating=20,
        defence_rating=20,
        form_rating=20,
        home_strength=20,
        away_strength=20,
    )

    fused = RatingFusionEngine().fuse(
        season,
        recent,
    )

    assert 20 <= fused.attack_rating <= 95
    assert 20 <= fused.defence_rating <= 95
    assert 20 <= fused.form_rating <= 95