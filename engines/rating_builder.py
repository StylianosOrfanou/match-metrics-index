from dataclasses import dataclass

from models.team_ratings import TeamRatings


@dataclass(frozen=True)
class TeamSeasonStatistics:
    name: str

    goals_for_per_game: float
    goals_against_per_game: float

    home_goals_for_per_game: float
    away_goals_for_per_game: float

    home_goals_against_per_game: float
    away_goals_against_per_game: float

    shots_per_game: float
    xg_per_game: float

    wins: int
    draws: int
    losses: int


class RatingBuilder:

    def build(
        self,
        teams: list[TeamSeasonStatistics],
    ) -> dict[str, TeamRatings]:
        if not teams:
            raise ValueError(
                "At least one team is required."
            )

        ratings = {}

        for team in teams:
            ratings[team.name] = TeamRatings(
                attack_rating=self._build_attack_rating(
                    team,
                    teams,
                ),
                defence_rating=self._build_defence_rating(
                    team,
                    teams,
                ),
                form_rating=self._build_form_rating(
                    team,
                    teams,
                ),
                home_strength=self._build_home_strength(
                    team,
                    teams,
                ),
                away_strength=self._build_away_strength(
                    team,
                    teams,
                ),
            )

        return ratings

    def _build_attack_rating(
        self,
        team: TeamSeasonStatistics,
        teams: list[TeamSeasonStatistics],
    ) -> float:
        goals_rating = self._normalize(
            value=team.goals_for_per_game,
            values=[
                item.goals_for_per_game
                for item in teams
            ],
        )

        xg_rating = self._normalize(
            value=team.xg_per_game,
            values=[
                item.xg_per_game
                for item in teams
            ],
        )

        shots_rating = self._normalize(
            value=team.shots_per_game,
            values=[
                item.shots_per_game
                for item in teams
            ],
        )

        return round(
            goals_rating * 0.50
            + xg_rating * 0.35
            + shots_rating * 0.15,
            2,
        )

    def _build_defence_rating(
        self,
        team: TeamSeasonStatistics,
        teams: list[TeamSeasonStatistics],
    ) -> float:
        return self._normalize(
            value=team.goals_against_per_game,
            values=[
                item.goals_against_per_game
                for item in teams
            ],
            reverse=True,
        )

    def _build_form_rating(
        self,
        team: TeamSeasonStatistics,
        teams: list[TeamSeasonStatistics],
    ) -> float:
        points_per_game = self._points_per_game(
            team
        )

        all_points_per_game = [
            self._points_per_game(item)
            for item in teams
        ]

        return self._normalize(
            value=points_per_game,
            values=all_points_per_game,
        )

    def _build_home_strength(
        self,
        team: TeamSeasonStatistics,
        teams: list[TeamSeasonStatistics],
    ) -> float:
        attack_rating = self._normalize(
            value=team.home_goals_for_per_game,
            values=[
                item.home_goals_for_per_game
                for item in teams
            ],
        )

        defence_rating = self._normalize(
            value=team.home_goals_against_per_game,
            values=[
                item.home_goals_against_per_game
                for item in teams
            ],
            reverse=True,
        )

        return round(
            attack_rating * 0.60
            + defence_rating * 0.40,
            2,
        )

    def _build_away_strength(
        self,
        team: TeamSeasonStatistics,
        teams: list[TeamSeasonStatistics],
    ) -> float:
        attack_rating = self._normalize(
            value=team.away_goals_for_per_game,
            values=[
                item.away_goals_for_per_game
                for item in teams
            ],
        )

        defence_rating = self._normalize(
            value=team.away_goals_against_per_game,
            values=[
                item.away_goals_against_per_game
                for item in teams
            ],
            reverse=True,
        )

        return round(
            attack_rating * 0.60
            + defence_rating * 0.40,
            2,
        )

    @staticmethod
    def _points_per_game(
        team: TeamSeasonStatistics,
    ) -> float:
        matches = (
            team.wins
            + team.draws
            + team.losses
        )

        if matches == 0:
            return 0.0

        return (
            team.wins * 3
            + team.draws
        ) / matches

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
            return round(
                (
                    minimum_rating
                    + maximum_rating
                ) / 2,
                2,
            )

        ratio = (
            value - minimum
        ) / (
            maximum - minimum
        )

        if reverse:
            ratio = 1 - ratio

        normalized = (
            minimum_rating
            + ratio
            * (
                maximum_rating
                - minimum_rating
            )
        )

        return round(
            normalized,
            2,
        )