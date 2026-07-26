from models.match import Match

from .team_factory import (
    create_team,
)


def create_match(
    home_team=None,
    away_team=None,
) -> Match:

    if home_team is None:
        home_team = create_team(
            name="Pafos FC",
        )

    if away_team is None:
        away_team = create_team(
            name="Omonia",
        )

    return Match(
        home_team=home_team,
        away_team=away_team,
    )