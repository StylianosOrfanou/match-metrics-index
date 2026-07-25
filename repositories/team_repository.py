from abc import ABC, abstractmethod

from models.team import Team


class TeamRepository(ABC):
    @abstractmethod
    def get_team(self, name: str) -> Team:
        """Return a team by name."""
        raise NotImplementedError


class InMemoryTeamRepository(TeamRepository):

    def __init__(self):
        self._teams = {}
        self._load_teams()