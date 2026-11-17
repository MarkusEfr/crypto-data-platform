import pytest
import requests

from crypto_data_platform.client import fetch_market
from unittest.mock import Mock, patch


def test_fetch_market_retries_timeout_then_succeeds():
    payload = {"data": [{"id": "90", "price_usd": "100.00"}]}

    response = Mock()
    response.status_code = 200
    response.json.return_value = payload

    with patch(
        "crypto_data_platform.client.requests.get",
        side_effect=[
            requests.exceptions.Timeout("Test timeout"),
            response,
        ],
    ) as mock_get:
        with patch("crypto_data_platform.client.time.sleep") as mock_sleep:
            result = fetch_market()

    assert result == payload
    assert mock_get.call_count == 2
    mock_sleep.assert_called_once_with(1.0)


from unittest.mock import call


def test_fetch_market_stops_after_three_timeouts():
    with patch(
        "crypto_data_platform.client.requests.get",
        side_effect=requests.exceptions.Timeout("Test timeout"),
    ) as mock_get:
        with patch("crypto_data_platform.client.time.sleep") as mock_sleep:
            with pytest.raises(requests.exceptions.Timeout):
                fetch_market()

    assert mock_get.call_count == 3
    assert mock_sleep.call_args_list == [
        call(1.0),
        call(2.0),
    ]


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
