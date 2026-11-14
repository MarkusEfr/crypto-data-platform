import logging

import requests

API_URL = "https://api.coinlore.net/api/tickers/"

logger = logging.getLogger(__name__)


def fetch_market(
    start: int = 0,
    limit: int = 20,
    timeout: int = 15,
) -> dict:
    if start < 0:
        raise ValueError("start must be non-negative")

    if limit <= 0:
        raise ValueError("limit must be positive")

    if timeout <= 0:
        raise ValueError("timeout must be positive")

    logger.debug(
        "Requesting market data: start=%s limit=%s",
        start,
        limit,
    )

    response = requests.get(
        API_URL,
        params={"start": start, "limit": limit},
        timeout=timeout,
    )
    response.raise_for_status()

    payload = response.json()

    if not isinstance(payload, dict):
        raise ValueError("Expected a JSON object")

    coins = payload.get("data")

    if not isinstance(coins, list) or not coins:
        raise ValueError("Expected a non-empty list in 'data'")

    logger.debug(
        "Requesting market data: start=%s limit=%s",
        start,
        limit,
    )
    return payload
