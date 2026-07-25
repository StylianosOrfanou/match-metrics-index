from engines.prediction_engine import predict_match

from models.match import Match
from models.team import Team

from presentation.terminal_presenter import (
    display_prediction
)


home_team = Team(
    name="Pafos",
    attack_rating=82,
    defence_rating=78,
    form_rating=80
)

away_team = Team(
    name="Omonia",
    attack_rating=75,
    defence_rating=80,
    form_rating=74
)

match = Match(
    home_team=home_team,
    away_team=away_team
)

prediction = predict_match(match)

display_prediction(prediction)