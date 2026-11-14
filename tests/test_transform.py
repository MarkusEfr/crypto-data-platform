from decimal import Decimal

from crypto_data_platform.transform import normalize_coin


def test_normalize_coin_converts_price():
    coin = {
        "id": "90",
        "symbol": "BTC",
        "name": "Bitcoin",
        "price_usd": "66819.17",
    }

    result = normalize_coin(coin)

    assert result == {
        "coin_id": "90",
        "symbol": "BTC",
        "name": "Bitcoin",
        "price_usd": Decimal("66819.17"),
    }
    assert isinstance(result["price_usd"], Decimal)
    assert coin["price_usd"] == "66819.17"
