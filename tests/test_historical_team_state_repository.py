from repositories.historical_team_state_repository import (
    HistoricalTeamStateRepository,
)


def test_unknown_team_receives_default_state():
    repository = HistoricalTeamStateRepository()

    state = repository.get_or_create(
        "Pafos FC"
    )

    assert state.name == "Pafos FC"
    assert state.elo_rating == 1500.0
    assert state.matches == 0


def test_same_team_returns_same_state():
    repository = HistoricalTeamStateRepository()

    first = repository.get_or_create(
        "Pafos FC"
    )

    second = repository.get_or_create(
        "Pafos FC"
    )

    assert first is second


def test_repository_updates_match_record():
    repository = HistoricalTeamStateRepository()

    repository.record_match(
        home_team="Pafos FC",
        away_team="Omonia",
        home_goals=2,
        away_goals=1,
    )

    pafos = repository.get_or_create(
        "Pafos FC"
    )

    omonia = repository.get_or_create(
        "Omonia"
    )

    assert pafos.matches == 1
    assert pafos.wins == 1
    assert pafos.goals_for == 2
    assert pafos.goals_against == 1

    assert omonia.matches == 1
    assert omonia.losses == 1
    assert omonia.goals_for == 1
    assert omonia.goals_against == 2


def test_repository_updates_home_and_away_records():
    repository = HistoricalTeamStateRepository()

    repository.record_match(
        home_team="Pafos FC",
        away_team="Omonia",
        home_goals=2,
        away_goals=1,
    )

    pafos = repository.get_or_create(
        "Pafos FC"
    )

    omonia = repository.get_or_create(
        "Omonia"
    )

    assert pafos.home_matches == 1
    assert pafos.home_goals_for == 2
    assert pafos.home_goals_against == 1

    assert omonia.away_matches == 1
    assert omonia.away_goals_for == 1
    assert omonia.away_goals_against == 2


def test_repository_returns_all_states():
    repository = HistoricalTeamStateRepository()

    repository.get_or_create(
        "Pafos FC"
    )

    repository.get_or_create(
        "Omonia"
    )

    states = repository.get_all()

    assert set(states) == {
        "Pafos FC",
        "Omonia",
    }