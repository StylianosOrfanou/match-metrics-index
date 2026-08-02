import pytest

from validation.historical_mmi_predictor import (
    HistoricalMMIPredictor,
)


def test_predictor_requires_components():
    with pytest.raises(
        TypeError,
    ):
        HistoricalMMIPredictor()

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