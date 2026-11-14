from decimal import Decimal, InvalidOperation


def normalize_market(payload: dict) -> list[dict]:
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a JSON object")
    if (
        "data" not in payload
        or not isinstance(payload["data"], list)
        or not payload["data"]
    ):
        raise ValueError("Payload must contain a non-empty 'data' list")

    normalized_coins = []
    for coin in payload.get("data", []):
        normalized_coins.append(normalize_coin(coin))
    return normalized_coins


def require_text(coin: dict, field: str) -> str:
    value = coin.get(field)

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")

    return value.strip()


def normalize_coin(coin: dict) -> dict:
    if not isinstance(coin, dict):
        raise ValueError("Each coin must be a JSON object")

    coin_id = require_text(coin, "id")
    symbol = require_text(coin, "symbol")
    name = require_text(coin, "name")
    price_text = require_text(coin, "price_usd")

    try:
        price = Decimal(price_text)
    except InvalidOperation as error:
        raise ValueError("price_usd must be a decimal number") from error

    if not price.is_finite() or price <= 0:
        raise ValueError("price_usd must be finite and positive")

    return {
        "coin_id": coin_id,
        "symbol": symbol,
        "name": name,
        "price_usd": price,
    }
