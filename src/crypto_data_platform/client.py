import logging
import time
import requests

API_URL = "https://api.coinlore.net/api/tickers/"

logger = logging.getLogger(__name__)

RETRYABLE_STATUSES = {500, 502, 503, 504}


def request_market(
    start: int,
    limit: int,
    timeout: int,
    max_attempts: int = 3,
    backoff_seconds: float = 1.0,
) -> requests.Response:
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")

    if backoff_seconds <= 0:
        raise ValueError("backoff_seconds must be positive")

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(
                API_URL,
                params={"start": start, "limit": limit},
                timeout=timeout,
            )

        except requests.exceptions.SSLError:
            # Помилку перевірки TLS не виправляємо повторами.
            raise

        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ) as error:
            if attempt == max_attempts:
                raise

            reason = type(error).__name__

        else:
            if response.status_code not in RETRYABLE_STATUSES:
                response.raise_for_status()
                return response

            if attempt == max_attempts:
                try:
                    response.raise_for_status()
                finally:
                    response.close()

            reason = f"HTTP {response.status_code}"
            response.close()

        delay = backoff_seconds * 2 ** (attempt - 1)

        logger.warning(
            "Request failed: attempt=%s/%s reason=%s; " "retrying in %.1f seconds",
            attempt,
            max_attempts,
            reason,
            delay,
        )

        time.sleep(delay)

    raise RuntimeError("Request loop ended unexpectedly")


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

    response = request_market(
        start=start,
        limit=limit,
        timeout=timeout,
    )

    try:
        payload = response.json()
    finally:
        response.close()

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
