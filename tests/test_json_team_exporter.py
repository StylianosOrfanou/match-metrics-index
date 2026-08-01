import json

import pytest

from exporters.json_team_exporter import (
    JsonTeamExporter,
)

from tests.helpers.team_factory import (
    create_team,
)


def test_exporter_writes_teams_to_json(
    tmp_path,
):
    file_path = tmp_path / "teams.json"

    teams = [
        create_team(
            name="Pafos FC",
            attack_rating=82,
            defence_rating=80,
            form_rating=78,
            home_strength=85,
            away_strength=81,
        ),
        create_team(
            name="Omonia",
            attack_rating=84,
            defence_rating=83,
            form_rating=86,
            home_strength=88,
            away_strength=85,
        ),
    ]

    exporter = JsonTeamExporter(
        file_path=str(file_path),
    )

    exporter.export(
        teams
    )

    data = json.loads(
        file_path.read_text(
            encoding="utf-8",
        )
    )

    assert len(data) == 2
    assert data[0]["name"] == "Pafos FC"
    assert data[0]["attack_rating"] == 82
    assert data[1]["name"] == "Omonia"


def test_exporter_writes_league_name(
    tmp_path,
):
    file_path = tmp_path / "teams.json"

    team = create_team(
        name="Pafos FC",
    )

    exporter = JsonTeamExporter(
        file_path=str(file_path),
    )

    exporter.export(
        [team]
    )

    data = json.loads(
        file_path.read_text(
            encoding="utf-8",
        )
    )

    assert (
        data[0]["league"]
        == "Cyprus First Division"
    )


def test_exporter_rejects_empty_list(
    tmp_path,
):
    file_path = tmp_path / "teams.json"

    exporter = JsonTeamExporter(
        file_path=str(file_path),
    )

    with pytest.raises(
        ValueError,
    ):
        exporter.export([])