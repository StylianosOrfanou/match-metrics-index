from dataclasses import dataclass

from models.recent_form import RecentForm


@dataclass(frozen=True)
class RecentFormRatings:
    attack_rating: float
    defence_rating: float
    form_rating: float
    home_strength: float
    away_strength: float


class RecentFormRatingBuilder:

    def build(
        self,
        recent_forms: dict[str, RecentForm],
    ) -> dict[str, RecentFormRatings]:
        if not recent_forms:
            raise ValueError(
                "At least one recent form is required."
            )

        goals_for_per_game = {
            name: self._safe_average(
                form.goals_for,
                form.matches,
            )
            for name, form in recent_forms.items()
        }

        goals_against_per_game = {
            name: self._safe_average(
                form.goals_against,
                form.matches,
            )
            for name, form in recent_forms.items()
        }

        points_per_game = {
            name: self._points_per_game(form)
            for name, form in recent_forms.items()
        }

        home_scoring = {
            name: self._safe_average(
                form.home_goals_for,
                form.home_matches,
            )
            for name, form in recent_forms.items()
        }

        home_defending = {
            name: self._safe_average(
                form.home_goals_against,
                form.home_matches,
            )
            for name, form in recent_forms.items()
        }

        away_scoring = {
            name: self._safe_average(
                form.away_goals_for,
                form.away_matches,
            )
            for name, form in recent_forms.items()
        }

        away_defending = {
            name: self._safe_average(
                form.away_goals_against,
                form.away_matches,
            )
            for name, form in recent_forms.items()
        }

        ratings: dict[str, RecentFormRatings] = {}

        for name in recent_forms:
            ratings[name] = RecentFormRatings(
                attack_rating=self._normalize(
                    value=goals_for_per_game[name],
                    values=list(
                        goals_for_per_game.values()
                    ),
                ),
                defence_rating=self._normalize(
                    value=goals_against_per_game[name],
                    values=list(
                        goals_against_per_game.values()
                    ),
                    reverse=True,
                ),
                form_rating=self._normalize(
                    value=points_per_game[name],
                    values=list(
                        points_per_game.values()
                    ),
                ),
                home_strength=self._combine_venue_rating(
                    attacking_value=home_scoring[name],
                    attacking_values=list(
                        home_scoring.values()
                    ),
                    defensive_value=home_defending[name],
                    defensive_values=list(
                        home_defending.values()
                    ),
                ),
                away_strength=self._combine_venue_rating(
                    attacking_value=away_scoring[name],
                    attacking_values=list(
                        away_scoring.values()
                    ),
                    defensive_value=away_defending[name],
                    defensive_values=list(
                        away_defending.values()
                    ),
                ),
            )

        return ratings

    def _combine_venue_rating(
        self,
        attacking_value: float,
        attacking_values: list[float],
        defensive_value: float,
        defensive_values: list[float],
    ) -> float:
        attacking_rating = self._normalize(
            value=attacking_value,
            values=attacking_values,
        )

        defensive_rating = self._normalize(
            value=defensive_value,
            values=defensive_values,
            reverse=True,
        )

        return round(
            attacking_rating * 0.60
            + defensive_rating * 0.40,
            2,
        )

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
        form: RecentForm,
    ) -> float:
        if form.matches == 0:
            return 0.0

        return (
            form.wins * 3
            + form.draws
        ) / form.matches

    @staticmethod
    def _normalize(
        value: float,
        values: list[float],
        reverse: bool = False,
    ) -> float:
        minimum = min(values)
        maximum = max(values)

        minimum_rating = 20.0
        maximum_rating = 95.0

        if maximum == minimum:
            return 57.5

        ratio = (
            value - minimum
        ) / (
            maximum - minimum
        )

        if reverse:
            ratio = 1 - ratio

        rating = (
            minimum_rating
            + ratio
            * (
                maximum_rating
                - minimum_rating
            )
        )

        return round(
            rating,
            2,
        )