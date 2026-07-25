def calculate_match_probabilities(
    home_probabilities,
    away_probabilities
):
    """
    Υπολογίζει:
    - Home Win
    - Draw
    - Away Win
    - Most Likely Score
    """

    home_win = 0.0
    draw = 0.0
    away_win = 0.0

    most_likely_score = None
    highest_score_probability = 0.0
    score_matrix = []

    for home_goals, home_probability in home_probabilities.items():
        for away_goals, away_probability in away_probabilities.items():

            score_probability = (
                home_probability * away_probability
            )
            score_matrix.append(
                {
                    "home_goals": home_goals,
                    "away_goals": away_goals,
                    "probability": score_probability
                }
            )

            if home_goals > away_goals:
                home_win += score_probability

            elif home_goals == away_goals:
                draw += score_probability

            else:
                away_win += score_probability

            if score_probability > highest_score_probability:
                highest_score_probability = score_probability
                most_likely_score = (
                    home_goals,
                    away_goals
                )

    total_probability = home_win + draw + away_win

    if total_probability > 0:
        home_win /= total_probability
        draw /= total_probability
        away_win /= total_probability

    score_matrix.sort(
        key=lambda x: x["probability"],
        reverse=True
    )

    return {
        "home_win": round(home_win * 100, 2),
        "draw": round(draw * 100, 2),
        "away_win": round(away_win * 100, 2),
        "most_likely_score": most_likely_score,
        "score_probability": round(
            highest_score_probability * 100,
            2
        ),
        "score_matrix": score_matrix
    }