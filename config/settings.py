# Team Rating weights
ATTACK_WEIGHT = 0.35
DEFENCE_WEIGHT = 0.35
FORM_WEIGHT = 0.30

# Matchup weights
MATCHUP_ATTACK_WEIGHT = 0.60
MATCHUP_DEFENCE_WEAKNESS_WEIGHT = 0.40

# Expected Goals settings
MIN_EXPECTED_GOALS = 0.20
MAX_EXPECTED_GOALS = 2.50
HOME_ADVANTAGE_XG = 0.20
ATTACK_WEIGHT = 0.60
FORM_WEIGHT = 0.20
VENUE_WEIGHT = 0.20
if not round(
    ATTACK_WEIGHT + FORM_WEIGHT + VENUE_WEIGHT,
    10,
) == 1:
    raise ValueError(
        "Matchup weights must total 1."
    )

# Poisson settings
MAX_GOALS = 8