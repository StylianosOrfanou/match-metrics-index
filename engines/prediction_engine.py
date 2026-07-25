from config.settings import MAX_GOALS

from engines.expected_goals import calculate_expected_goals
from engines.match_probabilities import calculate_match_probabilities
from engines.poisson import calculate_goal_probabilities

from models.match import Match
from models.team import Team
from models.matchup import calculate_matchup_rating
from models.prediction import (
    Prediction,
    ScorePrediction,
    TeamPrediction,
)


class PredictionEngine:

    def predict(self, match: Match) -> Prediction:
        if not isinstance(match, Match):
            raise TypeError("match must be a Match object.")

        home_team = match.home_team
        away_team = match.away_team

        home_matchup = self._calculate_matchup(
            team=home_team,
            opponent=away_team,
        )

        away_matchup = self._calculate_matchup(
            team=away_team,
            opponent=home_team,
        )

        home_xg = self._calculate_xg(
            matchup_rating=home_matchup,
            is_home=True,
        )

        away_xg = self._calculate_xg(
            matchup_rating=away_matchup,
            is_home=False,
        )

        home_goal_probabilities = calculate_goal_probabilities(
            expected_goals=home_xg,
            max_goals=MAX_GOALS,
        )

        away_goal_probabilities = calculate_goal_probabilities(
            expected_goals=away_xg,
            max_goals=MAX_GOALS,
        )

        match_probabilities = calculate_match_probabilities(
            home_probabilities=home_goal_probabilities,
            away_probabilities=away_goal_probabilities,
        )

        home_prediction = self._build_team_prediction(
            team=home_team,
            matchup_rating=home_matchup,
            expected_goals=home_xg,
        )

        away_prediction = self._build_team_prediction(
            team=away_team,
            matchup_rating=away_matchup,
            expected_goals=away_xg,
        )

        score_matrix = self._build_score_matrix(
            match_probabilities["score_matrix"]
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
            score_matrix=score_matrix,
        )

    def _calculate_matchup(
        self,
        team: Team,
        opponent: Team,
    ) -> float:
        return calculate_matchup_rating(
            team_attack=team.attack_rating,
            opponent_defence=opponent.defence_rating,
        )

    def _calculate_xg(
        self,
        matchup_rating: float,
        is_home: bool,
    ) -> float:
        return calculate_expected_goals(
            matchup_rating=matchup_rating,
            is_home=is_home,
        )

    def _build_team_prediction(
        self,
        team: Team,
        matchup_rating: float,
        expected_goals: float,
    ) -> TeamPrediction:
        return TeamPrediction(
            name=team.name,
            attack_rating=team.attack_rating,
            defence_rating=team.defence_rating,
            form_rating=team.form_rating,
            overall_rating=team.overall_rating,
            matchup_rating=matchup_rating,
            expected_goals=expected_goals,
        )

    def _build_score_matrix(
        self,
        scores: list[dict],
    ) -> list[ScorePrediction]:
        return [
            ScorePrediction(
                home_goals=score["home_goals"],
                away_goals=score["away_goals"],
                probability=score["probability"],
            )
            for score in scores
        ]