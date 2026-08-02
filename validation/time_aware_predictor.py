from abc import ABC
from abc import abstractmethod


class TimeAwarePredictor(
    ABC,
):

    @abstractmethod
    def predict(
        self,
        fixture,
    ) -> dict[str, float]:
        """
        Return match probabilities before the fixture
        result is known.
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        fixture,
    ) -> None:
        """
        Update the predictor state after the fixture
        has been completed.
        """
        raise NotImplementedError