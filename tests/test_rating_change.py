from models.rating_change import RatingChange


def test_rating_change_calculates_positive_difference():
    change = RatingChange(
        team_name="Pafos FC",
        metric="attack_rating",
        old_value=75.0,
        new_value=77.5,
    )

    assert change.difference == 2.5


def test_rating_change_calculates_negative_difference():
    change = RatingChange(
        team_name="Pafos FC",
        metric="defence_rating",
        old_value=80.0,
        new_value=77.25,
    )

    assert change.difference == -2.75