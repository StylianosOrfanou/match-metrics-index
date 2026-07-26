import json
from pathlib import Path
from typing import List

from models.validation_match import ValidationMatch
from repositories.validation_repository import (
    ValidationRepository,
)


class JsonValidationRepository(
    ValidationRepository,
):

    def __init__(
        self,
        file_path: str,
    ) -> None:
        self.file_path = Path(file_path)

    def get_all(self) -> List[ValidationMatch]:
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Validation file not found: "
                f"{self.file_path}"
            )

        with self.file_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "Validation data must be a JSON list."
            )

        return [
            self._create_validation_match(item)
            for item in data
        ]

    @staticmethod
    def _create_validation_match(
        data: dict,
    ) -> ValidationMatch:
        return ValidationMatch(
            date=data["date"],
            competition=data["competition"],
            home_team=data["home_team"],
            away_team=data["away_team"],
            home_goals=data["home_goals"],
            away_goals=data["away_goals"],
            bookmaker_home=data["bookmaker_home"],
            bookmaker_draw=data["bookmaker_draw"],
            bookmaker_away=data["bookmaker_away"],
        )