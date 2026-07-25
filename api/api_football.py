import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}


def search_team(team_name, country="Cyprus"):
    url = f"{BASE_URL}/teams"

    params = {
        "search": team_name
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()

    teams = data["response"]

    for item in teams:

        team = item["team"]

        if team["country"] == country:
            return team

    return None

from datetime import date, timedelta


def get_last_matches(team_id, season=2026):
    url = f"{BASE_URL}/fixtures"

    today = date.today()
    start_date = today - timedelta(days=365)

    params = {
        "team": team_id,
        "season": season,
        "from": start_date.isoformat(),
        "to": today.isoformat()
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()

    print("Errors:", data["errors"])
    print("Results:", data["results"])

    matches = data["response"]

    matches.sort(
        key=lambda match: match["fixture"]["date"],
        reverse=True
    )

    return matches[:10]