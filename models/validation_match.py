from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationMatch:
    """
    Represents a completed football match used
    to validate the MMI prediction engine.
    """

    date: str
    competition: str

    home_team: str
    away_team: str

    home_goals: int
    away_goals: int

    bookmaker_home: float
    bookmaker_draw: float
    bookmaker_away: float

    @property
    def result(self) -> str:
        if self.home_goals > self.away_goals:
            return "HOME"

        if self.home_goals < self.away_goals:
            return "AWAY"

        return "DRAW"