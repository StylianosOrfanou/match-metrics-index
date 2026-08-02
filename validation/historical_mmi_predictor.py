from engines.historical_rating_builder import (
    HistoricalRatingBuilder,
)
from engines.prediction_engine import (
    PredictionEngine,
)
from models.league import League
from models.match import Match
from repositories.historical_team_state_repository import (
    HistoricalTeamStateRepository,
)
from validation.time_aware_predictor import (
    TimeAwarePredictor,
)


class HistoricalMMIPredictor(
    TimeAwarePredictor,
):

    def __init__(
        self,
        state_repository:
        HistoricalTeamStateRepository,
        rating_builder:
        HistoricalRatingBuilder,
        league: League,
        prediction_engine:
        PredictionEngine,
    ) -> None:
        self._state_repository = (
            state_repository
        )
        self._rating_builder = (
            rating_builder
        )
        self._league = league
        self._prediction_engine = (
            prediction_engine
        )

    def predict(
        self,
        fixture: dict,
    ) -> dict[str, float]:
        home_team_name = fixture.get(
            "home_team"
        )
        away_team_name = fixture.get(
            "away_team"
        )

        if (
            not home_team_name
            or not away_team_name
        ):
            raise ValueError(
                "Fixture must contain home_team "
                "and away_team."
            )

        # Ensure both teams exist in the state
        # before ratings are generated.
        self._state_repository.get_or_create(
            home_team_name
        )
        self._state_repository.get_or_create(
            away_team_name
        )

        states = (
            self._state_repository.get_all()
        )

        teams = self._rating_builder.build_teams(
            states=states,
            league=self._league,
        )

        match = Match(
            home_team=teams[home_team_name],
            away_team=teams[away_team_name],
        )

        prediction = (
            self._prediction_engine.predict(
                match
            )
        )

        probabilities = {
            "H": prediction.home_win / 100,
            "D": prediction.draw / 100,
            "A": prediction.away_win / 100,
        }

        total_probability = sum(
            probabilities.values()
        )

        if total_probability <= 0:
            raise ValueError(
                "Prediction probabilities must "
                "total more than zero."
            )

        return {
            result: probability
            / total_probability
            for result, probability
            in probabilities.items()
        }

    def update(
        self,
        fixture: dict,
    ) -> None:
        home_team = fixture.get(
            "home_team"
        )
        away_team = fixture.get(
            "away_team"
        )
        home_goals = fixture.get(
            "home_goals"
        )
        away_goals = fixture.get(
            "away_goals"
        )

        if not home_team or not away_team:
            raise ValueError(
                "Fixture must contain home_team "
                "and away_team."
            )

        if (
            home_goals is None
            or away_goals is None
        ):
            raise ValueError(
                "Fixture must contain home_goals "
                "and away_goals."
            )

        self._state_repository.record_match(
            home_team=home_team,
            away_team=away_team,
            home_goals=home_goals,
            away_goals=away_goals,
        )

from engines.historical_rating_builder import (
    HistoricalRatingBuilder,
)
from engines.prediction_engine import (
    PredictionEngine,
)
from models.league import League
from repositories.historical_team_state_repository import (
    HistoricalTeamStateRepository,
)


def test_update_records_fixture_result():
    repository = (
        HistoricalTeamStateRepository()
    )

    predictor = HistoricalMMIPredictor(
        state_repository=repository,
        rating_builder=(
            HistoricalRatingBuilder()
        ),
        league=League(
            name="Cyprus First Division",
            country="Cyprus",
            average_goals=2.65,
            home_advantage=1.06,
        ),
        prediction_engine=(
            PredictionEngine()
        ),
    )

    predictor.update(
        {
            "home_team": "Pafos FC",
            "away_team": "Omonia",
            "home_goals": 2,
            "away_goals": 1,
        }
    )

    pafos = repository.get_or_create(
        "Pafos FC"
    )

    omonia = repository.get_or_create(
        "Omonia"
    )

    assert pafos.matches == 1
    assert pafos.wins == 1

    assert omonia.matches == 1
    assert omonia.losses == 1

def test_predict_returns_three_way_probabilities():
    predictor = HistoricalMMIPredictor(
        state_repository=(
            HistoricalTeamStateRepository()
        ),
        rating_builder=(
            HistoricalRatingBuilder()
        ),
        league=League(
            name="Cyprus First Division",
            country="Cyprus",
            average_goals=2.65,
            home_advantage=1.06,
        ),
        prediction_engine=(
            PredictionEngine()
        ),
    )

    probabilities = predictor.predict(
        {
            "home_team": "Pafos FC",
            "away_team": "Omonia",
        }
    )

    assert set(probabilities) == {
        "H",
        "D",
        "A",
    }

    assert sum(
        probabilities.values()
    ) == pytest.approx(
        1.0,
        abs=1e-6,
    )