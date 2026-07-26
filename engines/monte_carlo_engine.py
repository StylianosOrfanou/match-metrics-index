from collections import Counter
from dataclasses import dataclass
import random

from models.prediction import Prediction


@dataclass
class MonteCarloResult:
    simulations: int

    home_win: float
    draw: float
    away_win: float

    gg_probability: float
    over_25_probability: float
    under_25_probability: float

    average_home_goals: float
    average_away_goals: float
    average_total_goals: float

    most_common_score: tuple[int, int]
    most_common_score_probability: float


class MonteCarloEngine:
    def simulate(
        self,
        prediction: Prediction,
        simulations: int = 10_000,
        seed: int | None = None,
    ) -> MonteCarloResult:
        if simulations <= 0:
            raise ValueError(
                "Simulations must be greater than zero."
            )

        rng = random.Random(seed)

        home_wins = 0
        draws = 0
        away_wins = 0

        gg_count = 0
        over_25_count = 0

        total_home_goals = 0
        total_away_goals = 0

        score_counter: Counter[
            tuple[int, int]
        ] = Counter()

        for _ in range(simulations):
            home_goals, away_goals = (
                self._simulate_score(
                    prediction=prediction,
                    rng=rng,
                )
            )

            score_counter[
                (home_goals, away_goals)
            ] += 1

            total_home_goals += home_goals
            total_away_goals += away_goals

            if home_goals > away_goals:
                home_wins += 1
            elif home_goals == away_goals:
                draws += 1
            else:
                away_wins += 1

            if (
                home_goals > 0
                and away_goals > 0
            ):
                gg_count += 1

            if home_goals + away_goals > 2:
                over_25_count += 1

        most_common_score, score_count = (
            score_counter.most_common(1)[0]
        )

        home_win_probability = (
            home_wins / simulations
        )

        draw_probability = (
            draws / simulations
        )

        away_win_probability = (
            away_wins / simulations
        )

        gg_probability = (
            gg_count / simulations
        )

        over_25_probability = (
            over_25_count / simulations
        )

        average_home_goals = (
            total_home_goals / simulations
        )

        average_away_goals = (
            total_away_goals / simulations
        )

        return MonteCarloResult(
            simulations=simulations,
            home_win=round(
                home_win_probability,
                4,
            ),
            draw=round(
                draw_probability,
                4,
            ),
            away_win=round(
                away_win_probability,
                4,
            ),
            gg_probability=round(
                gg_probability,
                4,
            ),
            over_25_probability=round(
                over_25_probability,
                4,
            ),
            under_25_probability=round(
                1 - over_25_probability,
                4,
            ),
            average_home_goals=round(
                average_home_goals,
                2,
            ),
            average_away_goals=round(
                average_away_goals,
                2,
            ),
            average_total_goals=round(
                average_home_goals
                + average_away_goals,
                2,
            ),
            most_common_score=(
                most_common_score
            ),
            most_common_score_probability=round(
                score_count / simulations,
                4,
            ),
        )

    def _simulate_score(
        self,
        prediction: Prediction,
        rng: random.Random,
    ) -> tuple[int, int]:
        random_value = rng.random()
        cumulative_probability = 0.0

        for score in prediction.score_matrix:
            cumulative_probability += (
                score.probability
            )

            if (
                random_value
                <= cumulative_probability
            ):
                return (
                    score.home_goals,
                    score.away_goals,
                )

        final_score = prediction.score_matrix[-1]

        return (
            final_score.home_goals,
            final_score.away_goals,
        )