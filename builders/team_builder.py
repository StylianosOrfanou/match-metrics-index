from models.team import Team

from engines.rating_builder import (
    RatingBuilder,
    TeamSeasonStatistics,
)


class TeamBuilder:

    def __init__(
        self,
        rating_builder: RatingBuilder | None = None,
    ) -> None:
        self._rating_builder = (
            rating_builder
            or RatingBuilder()
        )

    def build(
        self,
        statistics: list[TeamSeasonStatistics],
        league,
    ) -> list[Team]:

        ratings = self._rating_builder.build(
            statistics,
        )

        teams = []

        for team_statistics in statistics:
            rating = ratings[
                team_statistics.name
            ]

            teams.append(
                Team(
                    name=team_statistics.name,
                    league=league,
                    attack_rating=rating.attack_rating,
                    defence_rating=rating.defence_rating,
                    form_rating=rating.form_rating,
                    home_strength=rating.home_strength,
                    away_strength=rating.away_strength,
                )
            )

        return teams