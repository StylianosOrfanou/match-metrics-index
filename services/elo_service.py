from engines.elo_engine import EloEngine
from engines.elo_rating_normalizer import (
    EloRatingNormalizer,
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
        normalizer: EloRatingNormalizer | None = None,
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
            or EloRatingNormalizer()
        )

    def build(
        self,
    ) -> dict[str, float]:

        matches = self._repository.get_all()

        elo = self._builder.build(
            matches
        )

        return self._normalizer.normalize(
            elo
        )