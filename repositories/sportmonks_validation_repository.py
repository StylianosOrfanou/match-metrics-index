from clients.sportmonks_client import SportmonksClient
from models.validation_match import ValidationMatch
from repositories.validation_repository import ValidationRepository


BET365_BOOKMAKER_ID = 2
MATCH_WINNER_MARKET_ID = 1

TEAM_NAME_MAPPING = {
    "AEL": "AEL Limassol",
    "Aris Limassol": "Aris",
    "Olympiakos": "Olympiakos Nicosia",
    "Krasava ENY Ypsonas FC": "Krasava ENY Ypsonas",
}

class SportmonksValidationRepository(ValidationRepository):

    def __init__(
        self,
        season_id: int,
        limit: int | None = None,
        client: SportmonksClient | None = None,
    ) -> None:
        self._season_id = season_id
        self._limit = limit
        self._client = client or SportmonksClient()

    def get_all(self) -> list[ValidationMatch]:
        fixtures = self._get_completed_fixtures()

        validation_matches: list[ValidationMatch] = []

        for index, fixture in enumerate(
            fixtures,
            start=1,
        ):
            if (
                self._limit is not None
                and len(validation_matches) >= self._limit
            ):
                break

            fixture_id = fixture["id"]

            print(
                f"Loading fixture {index}/{len(fixtures)}: "
                f"{fixture_id}"
            )

            validation_match = self._create_validation_match(
                fixture
            )

            if validation_match is not None:
                validation_matches.append(
                    validation_match
                )

        return validation_matches

    def _get_completed_fixtures(self) -> list[dict]:
        response = self._client.get(
            f"seasons/{self._season_id}",
            params={
                "include": (
                    "fixtures.participants;"
                    "fixtures.scores"
                ),
            },
        )

        season = response["data"]

        fixtures = season.get(
            "fixtures",
            [],
        )

        completed_fixtures: list[dict] = []

        for fixture in fixtures:
            home_goals = self._get_score(
                fixture,
                "home",
            )

            away_goals = self._get_score(
                fixture,
                "away",
            )

            if (
                home_goals is None
                or away_goals is None
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

    def _create_validation_match(
        self,
        fixture: dict,
    ) -> ValidationMatch | None:
        fixture_id = fixture["id"]

        odds = self._get_bet365_match_odds(
            fixture_id
        )

        if odds is None:
            print(
                f"Skipping fixture {fixture_id}: "
                "incomplete bet365 1X2 odds."
            )
            return None

        home_team = self._get_team_name(
            fixture,
            "home",
        )

        away_team = self._get_team_name(
            fixture,
            "away",
        )

        home_goals = self._get_score(
            fixture,
            "home",
        )

        away_goals = self._get_score(
            fixture,
            "away",
        )

        if (
            home_team is None
            or away_team is None
            or home_goals is None
            or away_goals is None
        ):
            print(
                f"Skipping fixture {fixture_id}: "
                "missing team or score data."
            )
            return None

        return ValidationMatch(
            date=fixture["starting_at"],
            competition=f"Season {self._season_id}",
            home_team=home_team,
            away_team=away_team,
            home_goals=home_goals,
            away_goals=away_goals,
            bookmaker_home=odds["Home"],
            bookmaker_draw=odds["Draw"],
            bookmaker_away=odds["Away"],
        )

    def _get_bet365_match_odds(
        self,
        fixture_id: int,
    ) -> dict[str, float] | None:
        response = self._client.get(
            f"odds/pre-match/fixtures/{fixture_id}"
        )

        odds_records = response.get(
            "data",
            [],
        )

        relevant_odds = [
            odd
            for odd in odds_records
            if (
                odd.get("bookmaker_id")
                == BET365_BOOKMAKER_ID
                and odd.get("market_id")
                == MATCH_WINNER_MARKET_ID
                and odd.get("label")
                in {"Home", "Draw", "Away"}
            )
        ]

        relevant_odds.sort(
            key=lambda odd: (
                odd.get(
                    "latest_bookmaker_update",
                    "",
                ),
                odd.get(
                    "created_at",
                    "",
                ),
            )
        )

        latest_odds: dict[str, float] = {}

        for odd in relevant_odds:
            label = odd.get("label")
            value = odd.get("value")

            if label is None:
                continue

            try:
                latest_odds[label] = float(value)
            except (TypeError, ValueError):
                continue

        required_labels = {
            "Home",
            "Draw",
            "Away",
        }

        if not required_labels.issubset(
            latest_odds
        ):
            return None

        return latest_odds

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

            if meta.get("location") == location:
                sportmonks_name = participant.get(
                    "name"
                )

                if sportmonks_name is None:
                    return None

                return TEAM_NAME_MAPPING.get(
                    sportmonks_name,
                    sportmonks_name,
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
                return score_data.get("goals")

        return None