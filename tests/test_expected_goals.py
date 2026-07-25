from config.settings import (
    MAX_EXPECTED_GOALS,
    MIN_EXPECTED_GOALS
)

from engines.expected_goals import calculate_expected_goals


def test_expected_goals_stays_inside_allowed_limits():
    expected_goals = calculate_expected_goals(
        matchup_rating=50,
        is_home=False
    )

    assert MIN_EXPECTED_GOALS <= expected_goals <= MAX_EXPECTED_GOALS


def test_higher_matchup_produces_higher_expected_goals():
    low_matchup_xg = calculate_expected_goals(
        matchup_rating=30,
        is_home=False
    )

    high_matchup_xg = calculate_expected_goals(
        matchup_rating=70,
        is_home=False
    )

    assert high_matchup_xg > low_matchup_xg


def test_home_team_receives_home_advantage():
    home_xg = calculate_expected_goals(
        matchup_rating=50,
        is_home=True
    )

    away_xg = calculate_expected_goals(
        matchup_rating=50,
        is_home=False
    )

    assert home_xg > away_xg


def test_zero_matchup_does_not_go_below_minimum_xg():
    expected_goals = calculate_expected_goals(
        matchup_rating=0,
        is_home=False
    )

    assert expected_goals >= MIN_EXPECTED_GOALS


def test_maximum_matchup_does_not_exceed_maximum_xg():
    expected_goals = calculate_expected_goals(
        matchup_rating=100,
        is_home=True
    )

    assert expected_goals <= MAX_EXPECTED_GOALS