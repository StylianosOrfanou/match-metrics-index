from datetime import datetime, timezone

from clients.sportmonks_client import SportmonksClient
from models.recent_form import RecentForm


class SportmonksRecentFormRepository:

    def __init__(
        self,
        season_id: int,
        client: SportmonksClient | None = None,
        matches_limit: int = 5,
    ) -> None:
        if matches_limit <= 0:
            raise ValueError(
                "matches_limit must be greater than zero."
            )

        self._season_id = season_id
        self._client = client or SportmonksClient()
        self._matches_limit = matches_limit

    def get_for_team(
        self,
        team_id: int,
    ) -> RecentForm:
        fixtures = self._get_completed_team_fixtures(
            team_id=team_id,
        )

        recent_fixtures = fixtures[
            -self._matches_limit:
        ]

        wins = 0
        draws = 0
        losses = 0

        goals_for = 0
        goals_against = 0

        home_matches = 0
        home_goals_for = 0
        home_goals_against = 0

        away_matches = 0
        away_goals_for = 0
        away_goals_against = 0

        for fixture in recent_fixtures:
            team_location = self._get_team_location(
                fixture=fixture,
                team_id=team_id,
            )

            if team_location is None:
                continue

            opponent_location = (
                "away"
                if team_location == "home"
                else "home"
            )

            team_goals = self._get_score(
                fixture=fixture,
                participant=team_location,
            )

            opponent_goals = self._get_score(
                fixture=fixture,
                participant=opponent_location,
            )

            if team_location == "home":
                home_matches += 1
                home_goals_for += team_goals
                home_goals_against += opponent_goals
            else:
                away_matches += 1
                away_goals_for += team_goals
                away_goals_against += opponent_goals

            if (
                team_goals is None
                or opponent_goals is None
            ):
                continue

            goals_for += team_goals
            goals_against += opponent_goals

            if team_goals > opponent_goals:
                wins += 1
            elif team_goals < opponent_goals:
                losses += 1
            else:
                draws += 1

        return RecentForm(
            matches=(
                wins
                + draws
                + losses
            ),
            wins=wins,
            draws=draws,
            losses=losses,
            goals_for=goals_for,
            goals_against=goals_against,
            home_matches=home_matches,
            home_goals_for=home_goals_for,
            home_goals_against=home_goals_against,
            away_matches=away_matches,
            away_goals_for=away_goals_for,
            away_goals_against=away_goals_against,
            expected_goals=0.0,
            shots=0,
        )

    def _get_completed_team_fixtures(
        self,
        team_id: int,
    ) -> list[dict]:
        response = self._client.get(
            f"seasons/{self._season_id}",
            params={
                "include": (
                    "fixtures.participants;"
                    "fixtures.scores"
                ),
            },
        )

        season = response.get(
            "data",
            {},
        )

        fixtures = season.get(
            "fixtures",
            [],
        )

        now = datetime.now(
            timezone.utc
        )

        completed_fixtures = []

        for fixture in fixtures:
            if not self._contains_team(
                fixture=fixture,
                team_id=team_id,
            ):
                continue

            starting_at = fixture.get(
                "starting_at"
            )

            if starting_at is None:
                continue

            fixture_date = datetime.strptime(
                starting_at,
                "%Y-%m-%d %H:%M:%S",
            ).replace(
                tzinfo=timezone.utc
            )

            if fixture_date >= now:
                continue

            home_score = self._get_score(
                fixture,
                "home",
            )

            away_score = self._get_score(
                fixture,
                "away",
            )

            if (
                home_score is None
                or away_score is None
            ):
                continue

            completed_fixtures.append(
                fixture
            )

        completed_fixtures.sort(
            key=lambda fixture: fixture.get(
                "starting_at",
                "",
            )
        )

        return completed_fixtures

    @staticmethod
    def _contains_team(
        fixture: dict,
        team_id: int,
    ) -> bool:
        return any(
            participant.get("id") == team_id
            for participant in fixture.get(
                "participants",
                [],
            )
        )

    @staticmethod
    def _get_team_location(
        fixture: dict,
        team_id: int,
    ) -> str | None:
        for participant in fixture.get(
            "participants",
            [],
        ):
            if participant.get("id") != team_id:
                continue

            return participant.get(
                "meta",
                {},
            ).get(
                "location"
            )

        return None

    @staticmethod
    def _get_score(
        fixture: dict,
        participant: str,
    ) -> int | None:
        for score in fixture.get(
            "scores",
            [],
        ):
            if score.get("description") != "CURRENT":
                continue

            score_data = score.get(
                "score",
                {},
            )

            if (
                score_data.get("participant")
                == participant
            ):
                return score_data.get(
                    "goals"
                )

        return None