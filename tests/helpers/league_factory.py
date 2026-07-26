from models.league import League


def create_league(
    name: str = "Cyprus First Division",
    country: str = "Cyprus",
    average_goals: float = 2.8,
    home_advantage: float = 1.10,
) -> League:
    return League(
        name=name,
        country=country,
        average_goals=average_goals,
        home_advantage=home_advantage,
    )