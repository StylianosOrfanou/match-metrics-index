import json
from pathlib import Path


class HistoricalFixtureRepository:

    def __init__(
        self,
        filepath: str | None = None,
    ) -> None:
        self._filepath = (
            Path(filepath)
            if filepath
            else Path(
                "data/historical_fixtures.json"
            )
        )

    def load(
        self,
    ) -> list[dict]:
        if not self._filepath.exists():
            return []

        with open(
            self._filepath,
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)