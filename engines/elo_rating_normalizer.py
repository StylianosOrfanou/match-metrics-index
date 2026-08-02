class EloRatingNormalizer:

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

    def normalize(
        self,
        ratings: dict[str, float],
    ) -> dict[str, float]:
        if not ratings:
            raise ValueError(
                "At least one Elo rating is required."
            )

        minimum_elo = min(
            ratings.values()
        )

        maximum_elo = max(
            ratings.values()
        )

        if maximum_elo == minimum_elo:
            midpoint = (
                self._minimum_rating
                + self._maximum_rating
            ) / 2

            return {
                team_name: round(
                    midpoint,
                    2,
                )
                for team_name in ratings
            }

        normalized_ratings = {}

        for team_name, elo_rating in (
            ratings.items()
        ):
            ratio = (
                elo_rating - minimum_elo
            ) / (
                maximum_elo - minimum_elo
            )

            normalized_rating = (
                self._minimum_rating
                + ratio
                * (
                    self._maximum_rating
                    - self._minimum_rating
                )
            )

            normalized_ratings[
                team_name
            ] = round(
                normalized_rating,
                2,
            )

        return normalized_ratings