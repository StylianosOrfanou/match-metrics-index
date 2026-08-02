from engines.elo_engine import EloEngine
from repositories.sportmonks_elo_repository import (
    SportmonksEloRepository,
)
from services.elo_builder_service import (
    EloBuilderService,
)


CYPRUS_SEASON_ID = 25996


def main() -> None:
    repository = SportmonksEloRepository(
        season_id=CYPRUS_SEASON_ID,
    )

    matches = repository.get_all()

    print()
    print("MMI ELO BUILD")
    print("-" * 60)
    print(f"Matches loaded: {len(matches)}")

    builder = EloBuilderService(
        elo_engine=EloEngine(
            k_factor=32,
            home_advantage=100,
        ),
        default_rating=1500,
    )

    ratings = builder.build(
        matches
    )

    print()
    print("CURRENT ELO RATINGS")
    print("-" * 60)

    for position, (
        team_name,
        rating,
    ) in enumerate(
        sorted(
            ratings.items(),
            key=lambda item: item[1],
            reverse=True,
        ),
        start=1,
    ):
        print(
            f"{position:>2}. "
            f"{team_name:<28} "
            f"{rating:.2f}"
        )


if __name__ == "__main__":
    main()