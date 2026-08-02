from engines.recent_form_rating_builder import (
    RecentFormRatings,
)
from models.team_ratings import TeamRatings
from models.team_signal import TeamSignal


class TeamSignalFactory:

    @staticmethod
    def from_season(
        ratings: TeamRatings,
        weight: float,
    ) -> TeamSignal:
        TeamSignalFactory._validate_weight(
            weight
        )

        return TeamSignal(
            attack=ratings.attack_rating,
            defence=ratings.defence_rating,
            form=ratings.form_rating,
            home_strength=ratings.home_strength,
            away_strength=ratings.away_strength,
            weight=weight,
        )

    @staticmethod
    def from_recent(
        ratings: RecentFormRatings,
        weight: float,
    ) -> TeamSignal:
        TeamSignalFactory._validate_weight(
            weight
        )

        return TeamSignal(
            attack=ratings.attack_rating,
            defence=ratings.defence_rating,
            form=ratings.form_rating,
            home_strength=ratings.home_strength,
            away_strength=ratings.away_strength,
            weight=weight,
        )

    @staticmethod
    def from_elo(
        elo_rating: float,
        weight: float,
    ) -> TeamSignal:
        TeamSignalFactory._validate_weight(
            weight
        )

        return TeamSignal(
            attack=elo_rating,
            defence=elo_rating,
            form=elo_rating,
            home_strength=elo_rating,
            away_strength=elo_rating,
            weight=weight,
        )

    @staticmethod
    def _validate_weight(
        weight: float,
    ) -> None:
        if weight <= 0:
            raise ValueError(
                "weight must be greater than zero."
            )