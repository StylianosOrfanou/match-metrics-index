import pytest

from validation.mmi_time_aware_predictor import (
    MMITimeAwarePredictor,
)


class FakePrediction:

    home_win = 50.0
    draw = 30.0
    away_win = 20.0


class FakeMatchService:

    def create_match(
        self,
        home_team_name,
        away_team_name,
    ):
        return (
            home_team_name,
            away_team_name,
        )


class FakePredictionEngine:

    def predict(
        self,
        match,
    ):
        return FakePrediction()


def test_predictor_returns_normalized_probabilities():
    predictor = MMITimeAwarePredictor(
        match_service=FakeMatchService(),
        prediction_engine=FakePredictionEngine(),
    )

    probabilities = predictor.predict(
        {
            "home_team": "Pafos FC",
            "away_team": "Omonia",
        }
    )

    assert probabilities == {
        "H": 0.50,
        "D": 0.30,
        "A": 0.20,
    }


def test_probabilities_sum_to_one():
    predictor = MMITimeAwarePredictor(
        match_service=FakeMatchService(),
        prediction_engine=FakePredictionEngine(),
    )

    probabilities = predictor.predict(
        {
            "home_team": "Pafos FC",
            "away_team": "Omonia",
        }
    )

    assert sum(
        probabilities.values()
    ) == pytest.approx(
        1.0,
        abs=1e-6,
    )


def test_predictor_requires_team_names():
    predictor = MMITimeAwarePredictor(
        match_service=FakeMatchService(),
        prediction_engine=FakePredictionEngine(),
    )

    with pytest.raises(ValueError):
        predictor.predict(
            {
                "home_team": "Pafos FC",
            }
        )