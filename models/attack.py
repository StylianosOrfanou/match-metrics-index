from statistics import pstdev


def calculate_attack_rating(goals_scored):
    """
    Υπολογίζει το Attack Rating από 0 έως 100.

    Τα αποτελέσματα δίνονται από το παλαιότερο
    προς το πιο πρόσφατο παιχνίδι.

    Παράδειγμα:
    [1, 2, 0, 3, 2]
    """

    if not goals_scored:
        return 0.0

    for goals in goals_scored:
        if not isinstance(goals, (int, float)):
            raise ValueError("Every goals value must be a number.")

        if goals < 0:
            raise ValueError("Goals cannot be negative.")

    # Περιορίζουμε την επίδραση ακραίων αποτελεσμάτων.
    # Για το rating, πάνω από 4 γκολ σε έναν αγώνα
    # δεν προσθέτουν επιπλέον αξία.
    capped_goals = [
        min(goals, 4)
        for goals in goals_scored
    ]

    weights = list(range(1, len(capped_goals) + 1))

    weighted_goals = sum(
        goals * weight
        for goals, weight in zip(capped_goals, weights)
    )

    total_weight = sum(weights)
    weighted_average = weighted_goals / total_weight

    # 3 γκολ ανά αγώνα αντιστοιχούν σε scoring rating 100.
    scoring_rating = min(
        (weighted_average / 3) * 100,
        100
    )

    matches_scored = sum(
        1 for goals in goals_scored
        if goals > 0
    )

    scoring_frequency = matches_scored / len(goals_scored)
    frequency_rating = scoring_frequency * 100

    # Μετρά πόσο αλλάζει η επιθετική παραγωγή από ματς σε ματς.
    variation = pstdev(capped_goals)

    # Με διακύμανση 3 ή μεγαλύτερη, η συνέπεια γίνεται 0.
    consistency_rating = max(
        0,
        100 - (variation / 3) * 100
    )

    final_rating = (
        scoring_rating * 0.60
        + frequency_rating * 0.25
        + consistency_rating * 0.15
    )

    return round(final_rating, 2)