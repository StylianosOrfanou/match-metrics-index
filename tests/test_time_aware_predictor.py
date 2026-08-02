from validation.time_aware_predictor import (
    TimeAwarePredictor,
)


class FakePredictor(
    TimeAwarePredictor,
):

    def predict(
        self,
        fixture,
    ):
        return {
            "H": 0.60,
            "D": 0.25,
            "A": 0.15,
        }

    def update(
        self,
        fixture,
    ):
        pass


def test_predictor_interface():
    predictor = FakePredictor()

    prediction = predictor.predict(
        {}
    )

    assert prediction["H"] == 0.60