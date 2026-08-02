from models.team_signal import TeamSignal


class WeightedRatingEngine:

    def combine(
        self,
        signals: list[TeamSignal],
    ) -> TeamSignal:
        if not signals:
            raise ValueError(
                "At least one signal is required."
            )

        total_weight = sum(
            signal.weight
            for signal in signals
        )

        if total_weight <= 0:
            raise ValueError(
                "Total weight must be greater than zero."
            )

        return TeamSignal(
            attack=self._weighted_average(
                signals,
                "attack",
                total_weight,
            ),
            defence=self._weighted_average(
                signals,
                "defence",
                total_weight,
            ),
            form=self._weighted_average(
                signals,
                "form",
                total_weight,
            ),
            home_strength=self._weighted_average(
                signals,
                "home_strength",
                total_weight,
            ),
            away_strength=self._weighted_average(
                signals,
                "away_strength",
                total_weight,
            ),
            weight=1.0,
        )

    @staticmethod
    def _weighted_average(
        signals: list[TeamSignal],
        attribute: str,
        total_weight: float,
    ) -> float:
        value = sum(
            getattr(signal, attribute)
            * signal.weight
            for signal in signals
        )

        return round(
            value / total_weight,
            2,
        )