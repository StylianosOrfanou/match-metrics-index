from clients.sportmonks_client import (
    SportmonksClient,
)


PAFOS_TEAM_ID = 8119
CYPRUS_SEASON_ID = 25996


def main() -> None:
    client = SportmonksClient()

    response = client.get(
        f"teams/{PAFOS_TEAM_ID}",
        params={
            "include": "statistics.details",
            "filters": (
                "teamStatisticSeasons:"
                f"{CYPRUS_SEASON_ID}"
            ),
        },
    )

    team = response["data"]

    print("\nPAFOS TEAM STATISTICS AUDIT")
    print("-" * 70)
    print(f"Team: {team.get('name')}")
    print(f"Team ID: {team.get('id')}")
    print(f"Season ID: {CYPRUS_SEASON_ID}")

    statistics = team.get(
        "statistics",
        [],
    )

    print(f"Statistics containers: {len(statistics)}")
    print("-" * 70)

    for statistic_group in statistics:
        print(
            f"\nSeason: "
            f"{statistic_group.get('season_id')}"
        )

        details = statistic_group.get(
            "details",
            [],
        )

        print(
            f"Details returned: {len(details)}"
        )

        for detail in details:
            print(
                f"type_id={detail.get('type_id')} | "
                f"value={detail.get('value')} | "
                f"name={detail.get('name')} | "
                f"code={detail.get('code')}"
            )


if __name__ == "__main__":
    main()