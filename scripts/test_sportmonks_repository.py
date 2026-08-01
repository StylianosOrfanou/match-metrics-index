from repositories.sportmonks_validation_repository import (
    SportmonksValidationRepository,
)


CYPRUS_SEASON_ID = 25996


def main() -> None:
    repository = SportmonksValidationRepository(
        season_id=CYPRUS_SEASON_ID,
        limit=5,
    )

    matches = repository.get_all()

    print("\nSPORTMONKS VALIDATION MATCHES")
    print("-" * 70)
    print(f"Matches created: {len(matches)}")
    print("-" * 70)

    for match in matches:
        print(
            f"{match.date} | "
            f"{match.home_team} "
            f"{match.home_goals}-"
            f"{match.away_goals} "
            f"{match.away_team} | "
            f"bet365: "
            f"{match.bookmaker_home} / "
            f"{match.bookmaker_draw} / "
            f"{match.bookmaker_away}"
        )


if __name__ == "__main__":
    main()