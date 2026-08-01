from clients.sportmonks_client import SportmonksClient

from engines.rating_builder import (
    TeamSeasonStatistics,
)


GOALS_FOR_TYPE_ID = 52
GOALS_AGAINST_TYPE_ID = 88
SHOTS_TYPE_ID = 1677
EXPECTED_GOALS_TYPE_ID = 5304

WINS_TYPE_ID = 214
DRAWS_TYPE_ID = 215
LOSSES_TYPE_ID = 216

MATCHES_PLAYED_TYPE_ID = 27263


class SportmonksTeamStatisticsRepository:

    def __init__(
        self,
        season_id: int,
        client: SportmonksClient | None = None,
    ) -> None:
        self._season_id = season_id
        self._client = client or SportmonksClient()

    def get_all(
        self,
    ) -> list[TeamSeasonStatistics]:
        teams = self._get_season_teams()

        statistics: list[TeamSeasonStatistics] = []

        for index, team in enumerate(
            teams,
            start=1,
        ):
            print(
                f"Loading team {index}/{len(teams)}: "
                f"{team['name']}"
            )

            team_statistics = (
                self._get_team_statistics(
                    team_id=team["id"],
                    team_name=team["name"],
                )
            )

            if team_statistics is not None:
                statistics.append(
                    team_statistics
                )

        return statistics

    def _get_season_teams(
        self,
    ) -> list[dict]:
        response = self._client.get(
            f"teams/seasons/{self._season_id}"
        )

        teams = response.get(
            "data",
            [],
        )

        teams.sort(
            key=lambda team: team.get(
                "name",
                "",
            )
        )

        return teams

    def _get_team_statistics(
        self,
        team_id: int,
        team_name: str,
    ) -> TeamSeasonStatistics | None:
        response = self._client.get(
            f"teams/{team_id}",
            params={
                "include": "statistics.details",
                "filters": (
                    "teamStatisticSeasons:"
                    f"{self._season_id}"
                ),
            },
        )

        team = response.get(
            "data",
            {},
        )

        statistics_groups = team.get(
            "statistics",
            [],
        )

        if not statistics_groups:
            print(
                f"Skipping {team_name}: "
                "no season statistics."
            )
            return None

        details = statistics_groups[0].get(
            "details",
            [],
        )

        goals_for = self._get_value(
            details,
            GOALS_FOR_TYPE_ID,
        )

        goals_against = self._get_value(
            details,
            GOALS_AGAINST_TYPE_ID,
        )

        shots = self._get_value(
            details,
            SHOTS_TYPE_ID,
        )

        expected_goals = self._get_value(
            details,
            EXPECTED_GOALS_TYPE_ID,
        )

        wins = self._get_value(
            details,
            WINS_TYPE_ID,
        )

        draws = self._get_value(
            details,
            DRAWS_TYPE_ID,
        )

        losses = self._get_value(
            details,
            LOSSES_TYPE_ID,
        )

        matches_played = self._get_value(
            details,
            MATCHES_PLAYED_TYPE_ID,
        )

        required_values = [
            goals_for,
            goals_against,
            shots,
            expected_goals,
            wins,
            draws,
            losses,
            matches_played,
        ]

        if any(
            value is None
            for value in required_values
        ):
            print(
                f"Skipping {team_name}: "
                "missing required statistics."
            )
            return None

        matches = matches_played.get(
            "total",
            0,
        )

        if not matches:
            print(
                f"Skipping {team_name}: "
                "zero matches played."
            )
            return None

        goals_for_all = goals_for.get(
            "all",
            {},
        )

        goals_against_all = goals_against.get(
            "all",
            {},
        )

        return TeamSeasonStatistics(
            name=self._map_team_name(
                team_name
            ),
            goals_for_per_game=float(
                goals_for_all.get(
                    "average",
                    0,
                )
            ),
            goals_against_per_game=float(
                goals_against_all.get(
                    "average",
                    0,
                )
            ),
            home_goals_for_per_game=float(
                goals_for.get(
                    "home",
                    {},
                ).get(
                    "average",
                    0,
                )
            ),
            away_goals_for_per_game=float(
                goals_for.get(
                    "away",
                    {},
                ).get(
                    "average",
                    0,
                )
            ),
            home_goals_against_per_game=float(
                goals_against.get(
                    "home",
                    {},
                ).get(
                    "average",
                    0,
                )
            ),
            away_goals_against_per_game=float(
                goals_against.get(
                    "away",
                    {},
                ).get(
                    "average",
                    0,
                )
            ),
            shots_per_game=float(
                shots.get(
                    "average",
                    0,
                )
            ),
            xg_per_game=round(
                float(
                    expected_goals.get(
                        "expected",
                        0,
                    )
                )
                / matches,
                4,
            ),
            wins=int(
                wins.get(
                    "all",
                    {},
                ).get(
                    "count",
                    0,
                )
            ),
            draws=int(
                draws.get(
                    "all",
                    {},
                ).get(
                    "count",
                    0,
                )
            ),
            losses=int(
                losses.get(
                    "all",
                    {},
                ).get(
                    "count",
                    0,
                )
            ),
        )

    @staticmethod
    def _get_value(
        details: list[dict],
        type_id: int,
    ) -> dict | None:
        for detail in details:
            if detail.get("type_id") == type_id:
                value = detail.get("value")

                if isinstance(value, dict):
                    return value

        return None

    @staticmethod
    def _map_team_name(
        team_name: str,
    ) -> str:
        mapping = {
            "Omonia Nicosia": "Omonia",
        }

        return mapping.get(
            team_name,
            team_name,
        )