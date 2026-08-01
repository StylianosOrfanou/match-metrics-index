from os import getenv

from dotenv import load_dotenv


load_dotenv()


# Sportmonks settings
SPORTMONKS_API_KEY = getenv(
    "SPORTMONKS_API_KEY"
)

BASE_URL = (
    "https://api.sportmonks.com/v3/football"
)


# Team Rating weights
ATTACK_WEIGHT = 0.60
DEFENCE_WEIGHT = 0.35
FORM_WEIGHT = 0.20
VENUE_WEIGHT = 0.20


# Matchup weights
MATCHUP_ATTACK_WEIGHT = 0.60
MATCHUP_DEFENCE_WEAKNESS_WEIGHT = 0.40


# Expected Goals settings
MIN_EXPECTED_GOALS = 0.20
MAX_EXPECTED_GOALS = 2.50
HOME_ADVANTAGE_XG = 0.20


# Poisson settings
MAX_GOALS = 8


if not round(
    ATTACK_WEIGHT
    + FORM_WEIGHT
    + VENUE_WEIGHT,
    10,
) == 1:
    raise ValueError(
        "Prediction weights must total 1."
    )


if not round(
    MATCHUP_ATTACK_WEIGHT
    + MATCHUP_DEFENCE_WEAKNESS_WEIGHT,
    10,
) == 1:
    raise ValueError(
        "Matchup weights must total 1."
    )