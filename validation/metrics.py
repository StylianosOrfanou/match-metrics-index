import math


def brier_score(
    predicted_probability: float,
    actual_outcome: int,
) -> float:
    if not 0 <= predicted_probability <= 1:
        raise ValueError(
            "predicted_probability must be between 0 and 1."
        )

    if actual_outcome not in {0, 1}:
        raise ValueError(
            "actual_outcome must be 0 or 1."
        )

    return round(
        (
            predicted_probability
            - actual_outcome
        ) ** 2,
        6,
    )

def three_way_brier_score(
    probabilities: dict[str, float],
    actual_result: str,
) -> float:
    valid_results = {
        "H",
        "D",
        "A",
    }

    if actual_result not in valid_results:
        raise ValueError(
            "actual_result must be H, D or A."
        )

    if set(probabilities.keys()) != valid_results:
        raise ValueError(
            "Probabilities must contain H, D and A."
        )

    total_probability = sum(
        probabilities.values()
    )

    if abs(total_probability - 1.0) > 1e-6:
        raise ValueError(
            "Probabilities must sum to 1."
        )

    score = 0.0

    for result in valid_results:
        observed = (
            1.0
            if result == actual_result
            else 0.0
        )

        score += (
            probabilities[result]
            - observed
        ) ** 2

    return round(
        score,
        6,
    )


def log_loss(
    predicted_probability: float,
    actual_outcome: int,
) -> float:
    if not 0 <= predicted_probability <= 1:
        raise ValueError(
            "predicted_probability must be between 0 and 1."
        )

    if actual_outcome not in {0, 1}:
        raise ValueError(
            "actual_outcome must be 0 or 1."
        )

    epsilon = 1e-15

    probability = min(
        max(
            predicted_probability,
            epsilon,
        ),
        1 - epsilon,
    )

    if actual_outcome == 1:
        loss = -math.log(
            probability
        )
    else:
        loss = -math.log(
            1 - probability
        )

    return round(
        loss,
        6,
    )

def three_way_log_loss(
    probabilities: dict[str, float],
    actual_result: str,
) -> float:
    valid_results = {
        "H",
        "D",
        "A",
    }

    if actual_result not in valid_results:
        raise ValueError(
            "actual_result must be H, D or A."
        )

    if set(probabilities) != valid_results:
        raise ValueError(
            "Probabilities must contain H, D and A."
        )

    for probability in probabilities.values():
        if not 0 <= probability <= 1:
            raise ValueError(
                "Every probability must be "
                "between 0 and 1."
            )

    total_probability = sum(
        probabilities.values()
    )

    if abs(total_probability - 1.0) > 1e-6:
        raise ValueError(
            "Probabilities must sum to 1."
        )

    epsilon = 1e-15

    actual_probability = max(
        probabilities[actual_result],
        epsilon,
    )

    return round(
        -math.log(actual_probability),
        6,
    )