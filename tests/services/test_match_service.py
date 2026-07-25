from repositories.in_memory_team_repository import (
    InMemoryTeamRepository,
)
from services.match_service import MatchService


def test_create_match():

    repository = InMemoryTeamRepository()
    service = MatchService(repository)

    match = service.create_match(
        "Aris Limassol",
        "Pafos FC",
    )

    assert match.home_team.name == "Aris Limassol"
    assert match.away_team.name == "Pafos FC"