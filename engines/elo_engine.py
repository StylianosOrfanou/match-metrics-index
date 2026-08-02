from models.elo_update import EloUpdate


class EloEngine:

    def __init__(
        self,
        k_factor: float = 32.0,
        home_advantage: float = 100.0,
    ) -> None:
        if k_factor <= 0:
            raise ValueError(
                "k_factor must be greater than zero."
            )

        if home_advantage < 0:
            raise ValueError(
                "home_advantage cannot be negative."
            )

        self._k_factor = k_factor
        self._home_advantage = home_advantage

    def expected_score(
        self,
        rating_a: float,
        rating_b: float,
    ) -> float:
        exponent = (
            rating_b - rating_a
        ) / 400

        return 1 / (
            1 + 10 ** exponent
        )

    def expected_home_score(
        self,
        home_rating: float,
        away_rating: float,
    ) -> float:
        adjusted_home_rating = (
            home_rating
            + self._home_advantage
        )

        return self.expected_score(
            rating_a=adjusted_home_rating,
            rating_b=away_rating,
        )

    def update_rating(
        self,
        rating: float,
        expected_score: float,
        actual_score: float,
    ) -> float:
        if not 0 <= expected_score <= 1:
            raise ValueError(
                "expected_score must be between 0 and 1."
            )

        if actual_score not in {
            0,
            0.5,
            1,
        }:
            raise ValueError(
                "actual_score must be 0, 0.5 or 1."
            )

        updated_rating = (
            rating
            + self._k_factor
            * (
                actual_score
                - expected_score
            )
        )

        return round(
            updated_rating,
            2,
        )

    def update_match(
        self,
        home_rating: float,
        away_rating: float,
        home_goals: int,
        away_goals: int,
    ) -> EloUpdate:
        if home_goals < 0 or away_goals < 0:
            raise ValueError(
                "Goals cannot be negative."
            )

        home_actual = self._get_actual_score(
            goals_for=home_goals,
            goals_against=away_goals,
        )

        away_actual = 1 - home_actual

        home_expected = self.expected_home_score(
            home_rating=home_rating,
            away_rating=away_rating,
        )

        away_expected = 1 - home_expected

        new_home_rating = self.update_rating(
            rating=home_rating,
            expected_score=home_expected,
            actual_score=home_actual,
        )

        new_away_rating = self.update_rating(
            rating=away_rating,
            expected_score=away_expected,
            actual_score=away_actual,
        )

        return EloUpdate(
            home_rating=new_home_rating,
            away_rating=new_away_rating,
            home_change=round(
                new_home_rating - home_rating,
                2,
            ),
            away_change=round(
                new_away_rating - away_rating,
                2,
            ),
        )

    @staticmethod
    def _get_actual_score(
        goals_for: int,
        goals_against: int,
    ) -> float:
        if goals_for > goals_against:
            return 1.0

        if goals_for < goals_against:
            return 0.0

        return 0.5