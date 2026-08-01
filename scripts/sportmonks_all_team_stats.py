from clients.sportmonks_client import SportmonksClient


CYPRUS_SEASON_ID = 25996

TEAM_IDS = {
    726: "AEK Larnaca",
    611: "AEL",
    2604: "APOEL",
    8171: "Akritas",
    272: "Anorthosis",
    6315: "Apollon",
    526: "Aris Limassol",
    2653: "Enosis",
    7608: "Ethnikos Achna",
    28636: "Krasava ENY Ypsonas FC",
    562: "Olympiakos",
    8122: "Omonia Aradippou",
    368: "Omonia Nicosia",
    8119: "Pafos FC",
}


def get_detail(
    details: list[dict],
    type_id: int,
) -> dict | None:
    for detail in details:
        if detail.get("type_id") == type_id:
            return detail.get("value")

    return None


def main() -> None:
    client = SportmonksClient()

    print("\nCYPRUS TEAM STATISTICS")
    print("-" * 110)

    for team_id, team_name in TEAM_IDS.items():
        response = client.get(
            f"teams/{team_id}",
            params={
                "include": "statistics.details",
                "filters": (
                    "teamStatisticSeasons:"
                    f"{CYPRUS_SEASON_ID}"
                ),
            },
        )

        team = response["data"]
        statistics = team.get("statistics", [])

        if not statistics:
            print(f"{team_name}: No statistics")
            continue

        details = statistics[0].get(
            "details",
            [],
        )

        goals = get_detail(details, 52) or {}
        conceded = get_detail(details, 88) or {}
        wins = get_detail(details, 214) or {}
        draws = get_detail(details, 215) or {}
        losses = get_detail(details, 216) or {}
        games = get_detail(details, 27263) or {}
        xg = get_detail(details, 5304) or {}
        rating = get_detail(details, 118) or {}

        print(
            f"{team_name:<28} | "
            f"MP {games.get('total', '?'):>2} | "
            f"GF {goals.get('all', {}).get('average', '?'):>4} | "
            f"GA {conceded.get('all', {}).get('average', '?'):>4} | "
            f"HGF {goals.get('home', {}).get('average', '?'):>4} | "
            f"AGF {goals.get('away', {}).get('average', '?'):>4} | "
            f"HGA {conceded.get('home', {}).get('average', '?'):>4} | "
            f"AGA {conceded.get('away', {}).get('average', '?'):>4} | "
            f"W {wins.get('all', {}).get('count', '?'):>2} | "
            f"D {draws.get('all', {}).get('count', '?'):>2} | "
            f"L {losses.get('all', {}).get('count', '?'):>2} | "
            f"xG {xg.get('expected', '?')} | "
            f"Rating {rating.get('value', '?')}"
        )


if __name__ == "__main__":
    main()