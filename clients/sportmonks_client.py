import requests

from config.settings import (
    BASE_URL,
    SPORTMONKS_API_KEY,
)


class SportmonksClient:

    def __init__(self) -> None:
        if not SPORTMONKS_API_KEY:
            raise ValueError(
                "SPORTMONKS_API_KEY was not found."
            )

    def get(
        self,
        endpoint: str,
        params: dict | None = None,
    ) -> dict:

        request_params = dict(params or {})
        request_params["api_token"] = SPORTMONKS_API_KEY

        response = requests.get(
            f"{BASE_URL}/{endpoint}",
            params=request_params,
            timeout=30,
        )

        if not response.ok:
            raise RuntimeError(
                f"Sportmonks request failed "
                f"({response.status_code}): "
                f"{response.text}"
            )

        return response.json()