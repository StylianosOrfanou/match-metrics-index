from engines.rating_normalizer import (
    RatingNormalizer,
)
from models import league
from models.historical_team_state import (
    HistoricalTeamState,
)
from models.team_ratings import (
    TeamRatings,
)
from models.league import League
from models.team import Team
from tests.test_team import league

class HistoricalRatingBuilder:

    def __init__(
        self,
        normalizer: RatingNormalizer | None = None,
    ) -> None:
        self._normalizer = (
            normalizer
            or RatingNormalizer()
        )

    def build(
        self,
        states: dict[
            str,
            HistoricalTeamState,
        ],
    ) -> dict[str, TeamRatings]:
        if not states:
            raise ValueError(
                "At least one historical "
                "team state is required."
            )

        attack_values = {
            name: self._safe_average(
                state.goals_for,
                state.matches,
            )
            for name, state in states.items()
        }

        defence_values = {
            name: self._safe_average(
                state.goals_against,
                state.matches,
            )
            for name, state in states.items()
        }

        form_values = {
            name: self._points_per_game(
                state
            )
            for name, state in states.items()
        }

        home_values = {
            name: self._venue_strength(
                goals_for=state.home_goals_for,
                goals_against=(
                    state.home_goals_against
                ),
                matches=state.home_matches,
            )
            for name, state in states.items()
        }

        away_values = {
            name: self._venue_strength(
                goals_for=state.away_goals_for,
                goals_against=(
                    state.away_goals_against
                ),
                matches=state.away_matches,
            )
            for name, state in states.items()
        }

        ratings: dict[str, TeamRatings] = {}

        for name in states:
            ratings[name] = TeamRatings(
                attack_rating=(
                    self._normalizer
                    .normalize_value(
                        value=attack_values[name],
                        values=list(
                            attack_values.values()
                        ),
                    )
                ),
                defence_rating=(
                    self._normalizer
                    .normalize_value(
                        value=defence_values[name],
                        values=list(
                            defence_values.values()
                        ),
                        reverse=True,
                    )
                ),
                form_rating=(
                    self._normalizer
                    .normalize_value(
                        value=form_values[name],
                        values=list(
                            form_values.values()
                        ),
                    )
                ),
                home_strength=(
                    self._normalizer
                    .normalize_value(
                        value=home_values[name],
                        values=list(
                            home_values.values()
                        ),
                    )
                ),
                away_strength=(
                    self._normalizer
                    .normalize_value(
                        value=away_values[name],
                        values=list(
                            away_values.values()
                        ),
                    )
                ),
            )

        return ratings

    def build_teams(
        self,
        states: dict[
            str,
            HistoricalTeamState,
        ],
        league: League,
    ) -> dict[str, Team]:
        ratings = self.build(
            states
        )

        return {
            team_name: Team(
                name=team_name,
                league=league,
                attack_rating=team_ratings.attack_rating,
                defence_rating=team_ratings.defence_rating,
                form_rating=team_ratings.form_rating,
                home_strength=team_ratings.home_strength,
                away_strength=team_ratings.away_strength,
            )
            for team_name, team_ratings
            in ratings.items()
        }    

    @staticmethod
    def _safe_average(
        total: int | float,
        matches: int,
    ) -> float:
        if matches == 0:
            return 0.0

        return total / matches

    @staticmethod
    def _points_per_game(
        state: HistoricalTeamState,
    ) -> float:
        if state.matches == 0:
            return 0.0

        return (
            state.wins * 3
            + state.draws
        ) / state.matches

    @staticmethod
    def _venue_strength(
        goals_for: int,
        goals_against: int,
        matches: int,
    ) -> float:
        if matches == 0:
            return 0.0

        goals_for_per_game = (
            goals_for / matches
        )

        goals_against_per_game = (
            goals_against / matches
        )

        return (
            goals_for_per_game
            - goals_against_per_game
        )