from builders.team_builder import TeamBuilder

from engines.rating_builder import (
    RatingBuilder,
    TeamSeasonStatistics,
)

from engines.rating_fusion_engine import (
    RatingFusionEngine,
)

from engines.recent_form_rating_builder import (
    RecentFormRatingBuilder,
)

from models.league import League
from models.recent_form import RecentForm
from models.team import Team
from models.team_ratings import TeamRatings


class RatingPipelineService:

    def __init__(
        self,
        season_rating_builder: RatingBuilder | None = None,
        recent_rating_builder:
        RecentFormRatingBuilder | None = None,
        fusion_engine: RatingFusionEngine | None = None,
        team_builder: TeamBuilder | None = None,
    ) -> None:
        self._season_rating_builder = (
            season_rating_builder
            or RatingBuilder()
        )

        self._recent_rating_builder = (
            recent_rating_builder
            or RecentFormRatingBuilder()
        )

        self._fusion_engine = (
            fusion_engine
            or RatingFusionEngine()
        )

        self._team_builder = (
            team_builder
            or TeamBuilder()
        )

    def build(
        self,
        season_statistics:
        list[TeamSeasonStatistics],
        recent_forms: dict[str, RecentForm],
        league: League,
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

        final_ratings = self._fuse_ratings(
            season_ratings=season_ratings,
            recent_ratings=recent_ratings,
        )

        return self._build_teams(
            season_statistics=season_statistics,
            final_ratings=final_ratings,
            league=league,
        )

    def _fuse_ratings(
        self,
        season_ratings: dict[str, TeamRatings],
        recent_ratings: dict,
    ) -> dict[str, TeamRatings]:
        final_ratings: dict[str, TeamRatings] = {}

        for team_name, season_rating in (
            season_ratings.items()
        ):
            recent_rating = recent_ratings.get(
                team_name
            )

            if recent_rating is None:
                final_ratings[team_name] = (
                    season_rating
                )
                continue

            final_ratings[team_name] = (
                self._fusion_engine.fuse(
                    season=season_rating,
                    recent=recent_rating,
                )
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