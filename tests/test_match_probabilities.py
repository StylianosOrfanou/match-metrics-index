import pytest

from engines.match_probabilities import calculate_match_probabilities
from engines.poisson import calculate_goal_probabilities


def create_prediction(home_xg, away_xg):
    home_probabilities = calculate_goal_probabilities(
        expected_goals=home_xg
    )

    away_probabilities = calculate_goal_probabilities(
        expected_goals=away_xg
    )

    return calculate_match_probabilities(
        home_probabilities=home_probabilities,
        away_probabilities=away_probabilities
    )


def test_match_probabilities_total_is_close_to_one_hundred():
    prediction = create_prediction(
        home_xg=1.72,
        away_xg=1.44
    )

    total_probability = (
        prediction["home_win"]
        + prediction["draw"]
        + prediction["away_win"]
    )

    assert total_probability == pytest.approx(
        100,
        abs=0.2
    )


def test_score_matrix_is_sorted_from_highest_to_lowest():
    prediction = create_prediction(
        home_xg=1.72,
        away_xg=1.44
    )

    score_matrix = prediction["score_matrix"]

    for index in range(len(score_matrix) - 1):
        current_probability = score_matrix[index]["probability"]
        next_probability = score_matrix[index + 1]["probability"]

        assert current_probability >= next_probability


def test_first_score_matches_most_likely_score():
    prediction = create_prediction(
        home_xg=1.72,
        away_xg=1.44
    )

    first_score = prediction["score_matrix"][0]

    expected_score = (
        first_score["home_goals"],
        first_score["away_goals"]
    )

    assert prediction["most_likely_score"] == expected_score


def test_equal_xg_produces_balanced_win_probabilities():
    prediction = create_prediction(
        home_xg=1.50,
        away_xg=1.50
    )

    assert prediction["home_win"] == pytest.approx(
        prediction["away_win"],
        abs=0.1
    )