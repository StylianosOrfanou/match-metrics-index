from dataclasses import dataclass

from models.team import Team


@dataclass
class Match:
    """
    Αντιπροσωπεύει έναν ποδοσφαιρικό αγώνα.
    """

    home_team: Team
    away_team: Team

    def __post_init__(self):
        if not isinstance(self.home_team, Team):
            raise TypeError(
                "home_team must be a Team object."
            )

        if not isinstance(self.away_team, Team):
            raise TypeError(
                "away_team must be a Team object."
            )

        if self.home_team.name == self.away_team.name:
            raise ValueError(
                "A team cannot play against itself."
            )