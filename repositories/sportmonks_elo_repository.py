from clients.sportmonks_client import SportmonksClient
from models.elo_match import EloMatch
from repositories.elo_repository import EloRepository


TEAM_NAME_MAPPING = {
    "Omonia Nicosia": "Omonia",
}


class SportmonksEloRepository(
    EloRepository,
):

    def __init__(
        self,
        season_id: int,
        client: SportmonksClient | None = None,
    ) -> None:
        self._season_id = season_id
        self._client = client or SportmonksClient()

    def get_all(
        self,
    ) -> list[EloMatch]:
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

        matches: list[EloMatch] = []

        for fixture in fixtures:
            elo_match = self._create_elo_match(
                fixture
            )

            if elo_match is not None:
                matches.append(
                    elo_match
                )

        matches.sort(
            key=lambda match: match.date
        )

        return matches

    def _create_elo_match(
        self,
        fixture: dict,
    ) -> EloMatch | None:
        home_team = self._get_team_name(
            fixture=fixture,
            location="home",
        )

        away_team = self._get_team_name(
            fixture=fixture,
            location="away",
        )

        home_goals = self._get_score(
            fixture=fixture,
            participant="home",
        )

        away_goals = self._get_score(
            fixture=fixture,
            participant="away",
        )

        date = fixture.get(
            "starting_at"
        )

        if (
            home_team is None
            or away_team is None
            or home_goals is None
            or away_goals is None
            or date is None
        ):
            return None

        return EloMatch(
            home_team=home_team,
            away_team=away_team,
            home_goals=home_goals,
            away_goals=away_goals,
            date=date,
        )

    @staticmethod
    def _get_team_name(
        fixture: dict,
        location: str,
    ) -> str | None:
        participants = fixture.get(
            "participants",
            [],
        )

        for participant in participants:
            meta = participant.get(
                "meta",
                {},
            )

            if meta.get("location") != location:
                continue

            name = participant.get("name")

            if name is None:
                return None

            return TEAM_NAME_MAPPING.get(
                name,
                name,
            )

        return None

    @staticmethod
    def _get_score(
        fixture: dict,
        participant: str,
    ) -> int | None:
        scores = fixture.get(
            "scores",
            [],
        )

        for score in scores:
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