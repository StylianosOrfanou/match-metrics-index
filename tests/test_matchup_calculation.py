from engines.prediction_engine import PredictionEngine
from models.league import League
from models.team import Team


league = League(
    name="Cyprus First Division",
    country="Cyprus",
    average_goals=2.65,
    home_advantage=1.06,
)


def create_team(
    attack=80,
    defence=80,
    form=80,
    home=80,
    away=80,
):
    return Team(
        name="Team",
        league=league,
        attack_rating=attack,
        defence_rating=defence,
        form_rating=form,
        home_strength=home,
        away_strength=away,
    )


def test_better_form_produces_higher_matchup():
    engine = PredictionEngine()
    opponent = create_team()

    low_form = create_team(form=60)
    high_form = create_team(form=90)

    low_matchup = engine._calculate_matchup(
        team=low_form,
        opponent=opponent,
        is_home=True,
    )

    high_matchup = engine._calculate_matchup(
        team=high_form,
        opponent=opponent,
        is_home=True,
    )

    assert high_matchup > low_matchup


def test_home_strength_affects_home_matchup():
    engine = PredictionEngine()
    opponent = create_team()

    weak_home = create_team(home=60)
    strong_home = create_team(home=90)

    weak_matchup = engine._calculate_matchup(
        team=weak_home,
        opponent=opponent,
        is_home=True,
    )

    strong_matchup = engine._calculate_matchup(
        team=strong_home,
        opponent=opponent,
        is_home=True,
    )

    assert strong_matchup > weak_matchup


def test_away_strength_affects_away_matchup():
    engine = PredictionEngine()
    opponent = create_team()

    weak_away = create_team(away=60)
    strong_away = create_team(away=90)

    weak_matchup = engine._calculate_matchup(
        team=weak_away,
        opponent=opponent,
        is_home=False,
    )

    strong_matchup = engine._calculate_matchup(
        team=strong_away,
        opponent=opponent,
        is_home=False,
    )

    assert strong_matchup > weak_matchup


def test_attack_rating_has_the_biggest_impact():
    engine = PredictionEngine()
    opponent = create_team()

    low_attack = create_team(attack=60)
    high_attack = create_team(attack=90)

    low_matchup = engine._calculate_matchup(
        team=low_attack,
        opponent=opponent,
        is_home=True,
    )

    high_matchup = engine._calculate_matchup(
        team=high_attack,
        opponent=opponent,
        is_home=True,
    )

    assert high_matchup > low_matchup