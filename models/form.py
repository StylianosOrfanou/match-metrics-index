def calculate_form_rating(results):
    """
    Υπολογίζει Form Rating από 0 έως 100.

    Το results πρέπει να περιέχει αποτελέσματα
    από το παλαιότερο προς το πιο πρόσφατο.

    Παράδειγμα:
    ["W", "D", "L", "W", "W"]
    """

    if not results:
        return 0.0

    points = {
        "W": 3,
        "D": 1,
        "L": 0
    }

    # Οι πιο πρόσφατοι αγώνες έχουν μεγαλύτερο βάρος.
    weights = list(range(1, len(results) + 1))

    weighted_points = 0
    maximum_points = 0

    for result, weight in zip(results, weights):
        result = result.upper()

        if result not in points:
            raise ValueError(
                f"Invalid result: {result}. Use only W, D or L."
            )

        weighted_points += points[result] * weight
        maximum_points += 3 * weight

    rating = (weighted_points / maximum_points) * 100

    return round(rating, 2)