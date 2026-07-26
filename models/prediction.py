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

    @property
    def total_xg(self) -> float:
        return round(
            self.home_team.expected_goals
            + self.away_team.expected_goals,
            2,
        )

    @property
    def gg_probability(self) -> float:
        return round(
            sum(
                score.probability
                for score in self.score_matrix
                if score.home_goals > 0
                and score.away_goals > 0
            ),
            2,
        )


    @property
    def over_05_probability(self) -> float:
        return self._calculate_over_probability(0)


    @property
    def over_15_probability(self) -> float:
        return self._calculate_over_probability(1)


    @property
    def over_25_probability(self) -> float:
        return self._calculate_over_probability(2)


    @property
    def over_35_probability(self) -> float:
        return self._calculate_over_probability(3)


    @property
    def under_25_probability(self) -> float:
        return self._calculate_under_probability(2)


    @property
    def under_35_probability(self) -> float:
        return self._calculate_under_probability(3)


    @property
    def home_or_draw_probability(self) -> float:
        return round(
            self.home_win + self.draw,
            2,
        )


    @property
    def away_or_draw_probability(self) -> float:
        return round(
            self.away_win + self.draw,
            2,
        )


    @property
    def no_draw_probability(self) -> float:
        return round(
            self.home_win + self.away_win,
            2,
        )


    def _calculate_over_probability(
        self,
        goal_limit: int,
    ) -> float:
        return round(
            sum(
                score.probability
                for score in self.score_matrix
                if (
                    score.home_goals
                    + score.away_goals
                ) > goal_limit
            ),
            2,
        )


    def _calculate_under_probability(
        self,
        goal_limit: int,
    ) -> float:
        return round(
            sum(
                score.probability
                for score in self.score_matrix
                if (
                    score.home_goals
                    + score.away_goals
                ) <= goal_limit
            ),
            2,
        )