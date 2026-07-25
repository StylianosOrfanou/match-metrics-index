import pytest

from engines.prediction_engine import PredictionEngine

from models.match import Match
from models.prediction import Prediction
from models.team import Team


@pytest.fixture
def home_team():
    return Team(
        name="Pafos",
        attack_rating=82,
        defence_rating=78,
        form_rating=80
    )


@pytest.fixture
def away_team():
    return Team(
        name="Omonia",
        attack_rating=75,
        defence_rating=80,
        form_rating=74
    )


@pytest.fixture
def match(home_team, away_team):
    return Match(
        home_team=home_team,
        away_team=away_team
    )


def test_engine_returns_prediction_object(match):
    engine = PredictionEngine()
    prediction = engine.predict(match)
    assert isinstance(prediction, Prediction)


def test_prediction_contains_both_teams(match):
    engine = PredictionEngine()
    prediction = engine.predict(match)

    assert prediction.home_team.name == "Pafos"
    assert prediction.away_team.name == "Omonia"


def test_prediction_contains_expected_goals(match):
    engine = PredictionEngine()
    prediction = engine.predict(match)

    assert prediction.home_team.expected_goals > 0
    assert prediction.away_team.expected_goals > 0


def test_prediction_probabilities_total_one_hundred(
    match
):
    engine = PredictionEngine()
    prediction = engine.predict(match)

    total_probability = (
        prediction.home_win
        + prediction.draw
        + prediction.away_win
    )

    assert total_probability == pytest.approx(
        100,
        abs=0.2
    )


def test_prediction_contains_score_matrix(match):
    engine = PredictionEngine()
    prediction = engine.predict(match)
    assert len(prediction.score_matrix) > 0


def test_prediction_rejects_invalid_match():
    engine = PredictionEngine()

    with pytest.raises(TypeError):
        engine.predict("Pafos vs Omonia")