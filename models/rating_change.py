from dataclasses import dataclass


@dataclass(frozen=True)
class RatingChange:
    team_name: str
    metric: str
    old_value: float
    new_value: float

    @property
    def difference(self) -> float:
        return round(
            self.new_value - self.old_value,
            2,
        )