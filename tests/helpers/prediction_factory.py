from models.prediction import (
    Prediction,
    ScorePrediction,
    TeamPrediction,
)

from .match_factory import (
    create_match,
)


def create_prediction(
    home_win: float = 0.50,
    draw: float = 0.25,
    away_win: float = 0.25,
    home_expected_goals: float = 1.60,
    away_expected_goals: float = 1.20,
) -> Prediction:
    match = create_match()

    home_team_prediction = TeamPrediction(
        name=match.home_team.name,
        attack_rating=80,
        defence_rating=80,
        form_rating=80,
        overall_rating=80,
        matchup_rating=60,
        expected_goals=home_expected_goals,
    )

    away_team_prediction = TeamPrediction(
        name=match.away_team.name,
        attack_rating=78,
        defence_rating=78,
        form_rating=78,
        overall_rating=78,
        matchup_rating=55,
        expected_goals=away_expected_goals,
    )

    score_matrix = [
        ScorePrediction(
            home_goals=0,
            away_goals=0,
            probability=0.10,
        ),
        ScorePrediction(
            home_goals=1,
            away_goals=0,
            probability=0.20,
        ),
        ScorePrediction(
            home_goals=1,
            away_goals=1,
            probability=0.15,
        ),
        ScorePrediction(
            home_goals=2,
            away_goals=1,
            probability=0.12,
        ),
    ]

    return Prediction(
        match=match,
        home_team=home_team_prediction,
        away_team=away_team_prediction,
        home_win=home_win,
        draw=draw,
        away_win=away_win,
        most_likely_score=(1, 0),
        score_probability=0.20,
        score_matrix=score_matrix,
    )