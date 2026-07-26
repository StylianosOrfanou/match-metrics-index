from engines.monte_carlo_engine import (
    MonteCarloResult,
)


def display_simulation(
    simulation: MonteCarloResult,
) -> None:
    print()
    print("MONTE CARLO SIMULATION")
    print("-" * 40)

    print(
        f"Simulations: "
        f"{simulation.simulations}"
    )

    print(
        f"Home Win: "
        f"{simulation.home_win:.2%}"
    )

    print(
        f"Draw: "
        f"{simulation.draw:.2%}"
    )

    print(
        f"Away Win: "
        f"{simulation.away_win:.2%}"
    )

    print(
        f"GG: "
        f"{simulation.gg_probability:.2%}"
    )

    print(
        f"Over 2.5: "
        f"{simulation.over_25_probability:.2%}"
    )

    print(
        f"Under 2.5: "
        f"{simulation.under_25_probability:.2%}"
    )

    print(
        f"Average Goals: "
        f"{simulation.average_home_goals}"
        f"-{simulation.average_away_goals}"
    )

    print(
        f"Average Total Goals: "
        f"{simulation.average_total_goals}"
    )

    home_goals, away_goals = (
        simulation.most_common_score
    )

    print(
        f"Most Common Score: "
        f"{home_goals}-{away_goals}"
    )

    print(
        f"Score Probability: "
        f"{simulation.most_common_score_probability:.2%}"
    )