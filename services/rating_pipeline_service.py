from config.settings import (
    ELO_SIGNAL_WEIGHT,
    RECENT_SIGNAL_WEIGHT,
    SEASON_SIGNAL_WEIGHT,
)
from engines.rating_builder import (
    RatingBuilder,
    TeamSeasonStatistics,
)
from engines.recent_form_rating_builder import (
    RecentFormRatingBuilder,
)
from engines.weighted_rating_engine import (
    WeightedRatingEngine,
)
from models.league import League
from models.recent_form import RecentForm
from models.team import Team
from models.team_ratings import TeamRatings
from services.team_signal_factory import (
    TeamSignalFactory,
)


class RatingPipelineService:

    def __init__(
        self,
        season_rating_builder: RatingBuilder | None = None,
        recent_rating_builder:
        RecentFormRatingBuilder | None = None,
        weighted_rating_engine:
        WeightedRatingEngine | None = None,
        signal_factory:
        TeamSignalFactory | None = None,
    ) -> None:
        self._season_rating_builder = (
            season_rating_builder
            or RatingBuilder()
        )

        self._recent_rating_builder = (
            recent_rating_builder
            or RecentFormRatingBuilder()
        )

        self._weighted_rating_engine = (
            weighted_rating_engine
            or WeightedRatingEngine()
        )

        self._signal_factory = (
            signal_factory
            or TeamSignalFactory()
        )

    def build(
        self,
        season_statistics:
        list[TeamSeasonStatistics],
        recent_forms: dict[str, RecentForm],
        league: League,
        elo_ratings: dict[str, float] | None = None,
    ) -> list[Team]:
        if not season_statistics:
            raise ValueError(
                "Season statistics cannot be empty."
            )

        if not recent_forms:
            raise ValueError(
                "Recent forms cannot be empty."
            )

        season_ratings = (
            self._season_rating_builder.build(
                season_statistics
            )
        )

        recent_ratings = (
            self._recent_rating_builder.build(
                recent_forms
            )
        )

        elo_ratings = elo_ratings or {}

        final_ratings = self._combine_ratings(
            season_ratings=season_ratings,
            recent_ratings=recent_ratings,
            elo_ratings=elo_ratings,
        )

        return self._build_teams(
            season_statistics=season_statistics,
            final_ratings=final_ratings,
            league=league,
        )

    def _combine_ratings(
        self,
        season_ratings: dict[str, TeamRatings],
        recent_ratings: dict,
        elo_ratings: dict[str, float],
    ) -> dict[str, TeamRatings]:
        final_ratings: dict[str, TeamRatings] = {}

        for team_name, season_rating in (
            season_ratings.items()
        ):
            signals = [
                self._signal_factory.from_season(
                    ratings=season_rating,
                    weight=SEASON_SIGNAL_WEIGHT,
                )
            ]

            recent_rating = recent_ratings.get(
                team_name
            )

            if recent_rating is not None:
                signals.append(
                    self._signal_factory.from_recent(
                        ratings=recent_rating,
                        weight=RECENT_SIGNAL_WEIGHT,
                    )
                )

            elo_rating = elo_ratings.get(
                team_name
            )

            if elo_rating is not None:
                signals.append(
                    self._signal_factory.from_elo(
                        elo_rating=elo_rating,
                        weight=ELO_SIGNAL_WEIGHT,
                    )
                )

            combined = (
                self._weighted_rating_engine.combine(
                    signals
                )
            )

            final_ratings[team_name] = TeamRatings(
                attack_rating=combined.attack,
                defence_rating=combined.defence,
                form_rating=combined.form,
                home_strength=combined.home_strength,
                away_strength=combined.away_strength,
            )

        return final_ratings

    @staticmethod
    def _build_teams(
        season_statistics:
        list[TeamSeasonStatistics],
        final_ratings: dict[str, TeamRatings],
        league: League,
    ) -> list[Team]:
        teams: list[Team] = []

        for statistics in season_statistics:
            rating = final_ratings[
                statistics.name
            ]

            teams.append(
                Team(
                    name=statistics.name,
                    league=league,
                    attack_rating=round(
                        rating.attack_rating,
                        2,
                    ),
                    defence_rating=round(
                        rating.defence_rating,
                        2,
                    ),
                    form_rating=round(
                        rating.form_rating,
                        2,
                    ),
                    home_strength=round(
                        rating.home_strength,
                        2,
                    ),
                    away_strength=round(
                        rating.away_strength,
                        2,
                    ),
                )
            )

        return teams