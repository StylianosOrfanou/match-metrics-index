class RatingNormalizer:

    def __init__(
        self,
        minimum_rating: float = 20.0,
        maximum_rating: float = 95.0,
    ) -> None:
        if minimum_rating >= maximum_rating:
            raise ValueError(
                "minimum_rating must be lower "
                "than maximum_rating."
            )

        self._minimum_rating = minimum_rating
        self._maximum_rating = maximum_rating

    def normalize_value(
        self,
        value: float,
        values: list[float],
        reverse: bool = False,
    ) -> float:
        if not values:
            raise ValueError(
                "At least one value is required."
            )

        minimum_value = min(values)
        maximum_value = max(values)

        if maximum_value == minimum_value:
            return round(
                (
                    self._minimum_rating
                    + self._maximum_rating
                )
                / 2,
                2,
            )

        ratio = (
            value - minimum_value
        ) / (
            maximum_value - minimum_value
        )

        if reverse:
            ratio = 1 - ratio

        rating = (
            self._minimum_rating
            + ratio
            * (
                self._maximum_rating
                - self._minimum_rating
            )
        )

        return round(
            rating,
            2,
        )

    def normalize_mapping(
        self,
        values: dict[str, float],
    ) -> dict[str, float]:
        if not values:
            raise ValueError(
                "At least one value is required."
            )

        all_values = list(
            values.values()
        )

        return {
            name: self.normalize_value(
                value=value,
                values=all_values,
            )
            for name, value in values.items()
        }
    