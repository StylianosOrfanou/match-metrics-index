from abc import ABC, abstractmethod

from models.league import League


class LeagueRepository(ABC):

    @abstractmethod
    def get_league(self, name: str) -> League:
        raise NotImplementedError