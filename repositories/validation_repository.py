from abc import ABC, abstractmethod
from typing import List

from models.validation_match import ValidationMatch


class ValidationRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[ValidationMatch]:
        """Return all historical validation matches."""
        raise NotImplementedError