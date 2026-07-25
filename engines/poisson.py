import math


def poisson_probability(expected_goals, goals):
    """
    Υπολογίζει την πιθανότητα μια ομάδα να σκοράρει
    ακριβώς έναν συγκεκριμένο αριθμό γκολ.

    expected_goals:
    Το xG της ομάδας.

    goals:
    Ο αριθμός γκολ που εξετάζουμε.
    """

    if not isinstance(expected_goals, (int, float)):
        raise ValueError("expected_goals must be a number.")

    if expected_goals < 0:
        raise ValueError("expected_goals cannot be negative.")

    if not isinstance(goals, int):
        raise ValueError("goals must be an integer.")

    if goals < 0:
        raise ValueError("goals cannot be negative.")

    probability = (
        math.exp(-expected_goals)
        * (expected_goals ** goals)
        / math.factorial(goals)
    )

    return probability


def calculate_goal_probabilities(
    expected_goals,
    max_goals=6
):
    """
    Επιστρέφει τις πιθανότητες από 0 έως max_goals.
    """

    if not isinstance(max_goals, int):
        raise ValueError("max_goals must be an integer.")

    if max_goals < 0:
        raise ValueError("max_goals cannot be negative.")

    probabilities = {}

    for goals in range(max_goals + 1):
        probability = poisson_probability(
            expected_goals=expected_goals,
            goals=goals
        )

        probabilities[goals] = probability

    return probabilities