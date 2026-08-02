from models.elo_match import EloMatch
from services.elo_service import EloService


class FakeRepository:

    def get_all(
        self,
    ) -> list[EloMatch]:
        return [
            EloMatch(
                home_team="Strong Team",
                away_team="Weak Team",
                home_goals=2,
                away_goals=0,
                date="2026-01-01",
            ),
        ]


def test_service_returns_dictionary():
    service = EloService(
        repository=FakeRepository(),
    )

    ratings = service.build()

    assert isinstance(
        ratings,
        dict,
    )


def test_service_returns_rating_for_every_team():
    service = EloService(
        repository=FakeRepository(),
    )

    ratings = service.build()

    assert "Strong Team" in ratings
    assert "Weak Team" in ratings


def test_winner_receives_higher_normalized_rating():
    service = EloService(
        repository=FakeRepository(),
    )

    ratings = service.build()

    assert (
        ratings["Strong Team"]
        > ratings["Weak Team"]
    )