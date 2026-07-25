from statistics import pstdev


def calculate_defence_rating(goals_conceded):
    """
    Υπολογίζει το Defence Rating από 0 έως 100.

    Τα γκολ παθητικό δίνονται από το παλαιότερο
    προς το πιο πρόσφατο παιχνίδι.

    Παράδειγμα:
    [1, 0, 2, 1, 0]
    """

    if not goals_conceded:
        return 0.0

    for goals in goals_conceded:
        if not isinstance(goals, (int, float)):
            raise ValueError("Every goals value must be a number.")

        if goals < 0:
            raise ValueError("Goals conceded cannot be negative.")

    # Περιορίζουμε την επίδραση ακραίων αποτελεσμάτων.
    capped_goals = [
        min(goals, 4)
        for goals in goals_conceded
    ]

    weights = list(range(1, len(capped_goals) + 1))

    weighted_goals_conceded = sum(
        goals * weight
        for goals, weight in zip(capped_goals, weights)
    )

    total_weight = sum(weights)
    weighted_average = weighted_goals_conceded / total_weight

    # 0 γκολ παθητικό = 100
    # 3 ή περισσότερα γκολ παθητικό ανά αγώνα = 0
    prevention_rating = max(
        0,
        100 - (weighted_average / 3) * 100
    )

    clean_sheets = sum(
        1 for goals in goals_conceded
        if goals == 0
    )

    clean_sheet_rating = (
        clean_sheets / len(goals_conceded)
    ) * 100

    # Μετρά τη σταθερότητα της αμυντικής απόδοσης.
    variation = pstdev(capped_goals)

    consistency_rating = max(
        0,
        100 - (variation / 3) * 100
    )

    final_rating = (
        prevention_rating * 0.65
        + clean_sheet_rating * 0.20
        + consistency_rating * 0.15
    )

    return round(final_rating, 2)