from engines.rating_normalizer import (
    RatingNormalizer,
)


class EloRatingNormalizer:

    def __init__(
        self,
        minimum_rating: float = 20.0,
        maximum_rating: float = 95.0,
    ) -> None:
        self._rating_normalizer = RatingNormalizer(
            minimum_rating=minimum_rating,
            maximum_rating=maximum_rating,
        )

    def normalize(
        self,
        ratings: dict[str, float],
    ) -> dict[str, float]:
        if not ratings:
            raise ValueError(
                "At least one Elo rating is required."
            )

        return (
            self._rating_normalizer
            .normalize_mapping(
                ratings
            )
        )