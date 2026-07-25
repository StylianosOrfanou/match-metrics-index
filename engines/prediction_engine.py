from config.settings import MAX_GOALS

from engines.expected_goals import calculate_expected_goals
from engines.match_probabilities import calculate_match_probabilities
from engines.poisson import calculate_goal_probabilities

from models.match import Match
from models.matchup import calculate_matchup_rating
from models.prediction import (
    Prediction,
    ScorePrediction,
    TeamPrediction
)


def predict_match(match: Match) -> Prediction:
    """
    Εκτελεί ολόκληρο το MMI prediction pipeline
    για έναν αγώνα.
    """

    if not isinstance(match, Match):
        raise TypeError(
            "match must be a Match object."
        )

    home_team = match.home_team
    away_team = match.away_team

    home_matchup = calculate_matchup_rating(
        team_attack=home_team.attack_rating,
        opponent_defence=away_team.defence_rating
    )

    away_matchup = calculate_matchup_rating(
        team_attack=away_team.attack_rating,
        opponent_defence=home_team.defence_rating
    )

    home_xg = calculate_expected_goals(
        matchup_rating=home_matchup,
        is_home=True
    )

    away_xg = calculate_expected_goals(
        matchup_rating=away_matchup,
        is_home=False
    )

    home_goal_probabilities = calculate_goal_probabilities(
        expected_goals=home_xg,
        max_goals=MAX_GOALS
    )

    away_goal_probabilities = calculate_goal_probabilities(
        expected_goals=away_xg,
        max_goals=MAX_GOALS
    )

    match_probabilities = calculate_match_probabilities(
        home_probabilities=home_goal_probabilities,
        away_probabilities=away_goal_probabilities
    )

    home_prediction = TeamPrediction(
        name=home_team.name,
        attack_rating=home_team.attack_rating,
        defence_rating=home_team.defence_rating,
        form_rating=home_team.form_rating,
        overall_rating=home_team.overall_rating,
        matchup_rating=home_matchup,
        expected_goals=home_xg
    )

    away_prediction = TeamPrediction(
        name=away_team.name,
        attack_rating=away_team.attack_rating,
        defence_rating=away_team.defence_rating,
        form_rating=away_team.form_rating,
        overall_rating=away_team.overall_rating,
        matchup_rating=away_matchup,
        expected_goals=away_xg
    )

    score_matrix = []

    for score in match_probabilities["score_matrix"]:
        score_matrix.append(
            ScorePrediction(
                home_goals=score["home_goals"],
                away_goals=score["away_goals"],
                probability=score["probability"]
            )
        )

    return Prediction(
        match=match,
        home_team=home_prediction,
        away_team=away_prediction,
        home_win=match_probabilities["home_win"],
        draw=match_probabilities["draw"],
        away_win=match_probabilities["away_win"],
        most_likely_score=(
            match_probabilities["most_likely_score"]
        ),
        score_probability=(
            match_probabilities["score_probability"]
        ),
        score_matrix=score_matrix
    )