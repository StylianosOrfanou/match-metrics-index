from models.historical_team_state import (
    HistoricalTeamState,
)


class HistoricalTeamStateRepository:

    def __init__(self) -> None:
        self._states: dict[
            str,
            HistoricalTeamState,
        ] = {}

    def get_or_create(
        self,
        team_name: str,
    ) -> HistoricalTeamState:
        if team_name not in self._states:
            self._states[team_name] = (
                HistoricalTeamState(
                    name=team_name,
                )
            )

        return self._states[team_name]

    def record_match(
        self,
        home_team: str,
        away_team: str,
        home_goals: int,
        away_goals: int,
    ) -> None:
        home = self.get_or_create(
            home_team
        )

        away = self.get_or_create(
            away_team
        )

        home.matches += 1
        away.matches += 1

        home.goals_for += home_goals
        home.goals_against += away_goals

        away.goals_for += away_goals
        away.goals_against += home_goals

        if home_goals > away_goals:
            home.wins += 1
            away.losses += 1

        elif home_goals < away_goals:
            away.wins += 1
            home.losses += 1

        else:
            home.draws += 1
            away.draws += 1