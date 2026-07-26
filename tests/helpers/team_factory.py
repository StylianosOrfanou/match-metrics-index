from models.team import Team

from .league_factory import (
    create_league,
)


def create_team(
    name: str = "Pafos FC",
    attack_rating: float = 80,
    defence_rating: float = 80,
    form_rating: float = 80,
    home_strength: float = 80,
    away_strength: float = 80,
    league=None,
) -> Team:

    if league is None:
        league = create_league()

    return Team(
        name=name,
        league=league,
        attack_rating=attack_rating,
        defence_rating=defence_rating,
        form_rating=form_rating,
        home_strength=home_strength,
        away_strength=away_strength,
    )