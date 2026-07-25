from models.prediction import Prediction


def display_prediction(prediction: Prediction):
    """
    Εμφανίζει την πρόβλεψη στο terminal.
    """

    home_score, away_score = prediction.most_likely_score

    print("-" * 40)
    print("MMI MATCH PREDICTION")
    print("-" * 40)

    print(
        f"{prediction.home_team.name} Overall Rating: "
        f"{prediction.home_team.overall_rating}/100"
    )

    print(
        f"{prediction.away_team.name} Overall Rating: "
        f"{prediction.away_team.overall_rating}/100"
    )

    print(
        f"{prediction.home_team.name} Matchup: "
        f"{prediction.home_team.matchup_rating}/100"
    )

    print(
        f"{prediction.away_team.name} Matchup: "
        f"{prediction.away_team.matchup_rating}/100"
    )

    print(
        f"{prediction.home_team.name} xG: "
        f"{prediction.home_team.expected_goals}"
    )

    print(
        f"{prediction.away_team.name} xG: "
        f"{prediction.away_team.expected_goals}"
    )

    print(f"Home Win: {prediction.home_win}%")
    print(f"Draw: {prediction.draw}%")
    print(f"Away Win: {prediction.away_win}%")

    print(
        f"Most Likely Score: "
        f"{home_score}-{away_score}"
    )

    print(
        f"Score Probability: "
        f"{prediction.score_probability}%"
    )

    print("\nTop 5 Most Likely Scores")
    print("-" * 40)

    for score in prediction.score_matrix[:5]:
        print(
            f"{score.home_goals}-"
            f"{score.away_goals} : "
            f"{score.probability * 100:.2f}%"
        )