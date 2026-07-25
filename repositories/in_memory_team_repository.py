from models.team import Team
from repositories.team_repository import TeamRepository


class InMemoryTeamRepository(TeamRepository):

    def __init__(self):
        self._teams = {}
        self._load_teams()

    def _load_teams(self):
        aris = Team(
            name="Aris Limassol",
            attack_rating=80,
            defence_rating=75,
            form_rating=85,
        )

        pafos = Team(
            name="Pafos FC",
            attack_rating=82,
            defence_rating=80,
            form_rating=78,
        )

        omonia = Team(
            name="Omonia",
            attack_rating=79,
            defence_rating=74,
            form_rating=81,
        )

        self._teams[aris.name] = aris
        self._teams[pafos.name] = pafos
        self._teams[omonia.name] = omonia

    def get_team(self, name: str) -> Team:
        if name not in self._teams:
            raise ValueError(f"Team '{name}' was not found.")

        return self._teams[name]