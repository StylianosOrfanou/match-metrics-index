from abc import ABC
from abc import abstractmethod

from models.elo_match import EloMatch


class EloRepository(
    ABC,
):

    @abstractmethod
    def get_all(
        self,
    ) -> list[EloMatch]:
        pass