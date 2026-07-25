from dataclasses import dataclass
from typing import List, Tuple

from models.match import Match


@dataclass
class TeamPrediction:
    """
    Τα υπολογισμένα δεδομένα μίας ομάδας
    για έναν συγκεκριμένο αγώνα.
    """

    name: str
    attack_rating: float
    defence_rating: float
    form_rating: float
    overall_rating: float
    matchup_rating: float
    expected_goals: float


@dataclass
class ScorePrediction:
    """
    Η πιθανότητα ενός συγκεκριμένου σκορ.
    """

    home_goals: int
    away_goals: int
    probability: float


@dataclass
class Prediction:
    """
    Το τελικό αποτέλεσμα του MMI Prediction Engine.
    """

    match: Match

    home_team: TeamPrediction
    away_team: TeamPrediction

    home_win: float
    draw: float
    away_win: float

    most_likely_score: Tuple[int, int]
    score_probability: float

    score_matrix: List[ScorePrediction]