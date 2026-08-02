from engines.elo_engine import EloEngine
from engines.rating_normalizer import (
    RatingNormalizer,
)
from repositories.elo_repository import (
    EloRepository,
)
from services.elo_builder_service import (
    EloBuilderService,
)


class EloService:

    def __init__(
        self,
        repository: EloRepository,
        builder: EloBuilderService | None = None,
        normalizer: RatingNormalizer | None = None,
    ) -> None:

        self._repository = repository

        self._builder = (
            builder
            or EloBuilderService(
                elo_engine=EloEngine(),
            )
        )

        self._normalizer = (
            normalizer
            or RatingNormalizer()
        )

    def build(
        self,
    ) -> dict[str, float]:

        matches = self._repository.get_all()

        elo = self._builder.build(
            matches
        )

        return self._normalizer.normalize_mapping(
            elo
        )