from engines.elo_engine import EloEngine
from models.elo_match import EloMatch


class EloBuilderService:

    def __init__(
        self,
        elo_engine: EloEngine | None = None,
        default_rating: float = 1500.0,
    ) -> None:
        if default_rating <= 0:
            raise ValueError(
                "default_rating must be greater than zero."
            )

        self._elo_engine = elo_engine or EloEngine()
        self._default_rating = default_rating

    def build(
        self,
        matches: list[EloMatch],
    ) -> dict[str, float]:
        ratings: dict[str, float] = {}

        sorted_matches = sorted(
            matches,
            key=lambda match: match.date,
        )

        for match in sorted_matches:
            home_rating = ratings.get(
                match.home_team,
                self._default_rating,
            )

            away_rating = ratings.get(
                match.away_team,
                self._default_rating,
            )

            update = self._elo_engine.update_match(
                home_rating=home_rating,
                away_rating=away_rating,
                home_goals=match.home_goals,
                away_goals=match.away_goals,
            )

            ratings[match.home_team] = (
                update.home_rating
            )

            ratings[match.away_team] = (
                update.away_rating
            )

        return ratings
    