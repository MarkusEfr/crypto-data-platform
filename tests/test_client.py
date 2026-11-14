import pytest
import requests

from crypto_data_platform.client import fetch_market
from unittest.mock import Mock, patch


def test_fetch_market_returns_payload():
    expected_payload = {
        "data": [
            {
                "id": "90",
                "name": "Bitcoin",
                "price_usd": "100.00",
            }
        ],
        "info": {"coins_num": 1},
    }

    fake_response = Mock()
    fake_response.json.return_value = expected_payload

    with patch(
        "crypto_data_platform.client.requests.get",
        return_value=fake_response,
    ):
        result = fetch_market(limit=1)

    assert result == expected_payload
    fake_response.raise_for_status.assert_called_once()


def test_fetch_market_propagates_timeout():
    with patch(
        "crypto_data_platform.client.requests.get",
        side_effect=requests.exceptions.Timeout("Test timeout"),
    ):
        with pytest.raises(requests.exceptions.Timeout):
            fetch_market()


def test_fetch_market_rejects_zero_limit():
    with pytest.raises(ValueError, match="limit must be positive"):
        fetch_market(limit=0)
