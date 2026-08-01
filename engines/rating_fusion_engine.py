from models.team_ratings import TeamRatings

from engines.recent_form_rating_builder import (
    RecentFormRatings,
)

from config.settings import (
    SEASON_ATTACK_WEIGHT,
    RECENT_ATTACK_WEIGHT,
    SEASON_DEFENCE_WEIGHT,
    RECENT_DEFENCE_WEIGHT,
    SEASON_FORM_WEIGHT,
    RECENT_FORM_WEIGHT,
    SEASON_HOME_WEIGHT,
    RECENT_HOME_WEIGHT,
    SEASON_AWAY_WEIGHT,
    RECENT_AWAY_WEIGHT,
)


class RatingFusionEngine:

    def fuse(
        self,
        season: TeamRatings,
        recent: RecentFormRatings,
    ) -> TeamRatings:

        return TeamRatings(
            attack_rating=(
                season.attack_rating
                * SEASON_ATTACK_WEIGHT
                + recent.attack_rating
                * RECENT_ATTACK_WEIGHT
            ),

            defence_rating=(
                season.defence_rating
                * SEASON_DEFENCE_WEIGHT
                + recent.defence_rating
                * RECENT_DEFENCE_WEIGHT
            ),

            form_rating=(
                season.form_rating
                * SEASON_FORM_WEIGHT
                + recent.form_rating
                * RECENT_FORM_WEIGHT
            ),

            home_strength=(
                season.home_strength
                * SEASON_HOME_WEIGHT
                + recent.home_strength
                * RECENT_HOME_WEIGHT
            ),

            away_strength=(
                season.away_strength
                * SEASON_AWAY_WEIGHT
                + recent.away_strength
                * RECENT_AWAY_WEIGHT
            ),
        )