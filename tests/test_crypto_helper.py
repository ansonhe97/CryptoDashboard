'''
@Author:	Jiawei He(Anson)
@Date:		2023/11/26

Unit tests for crypto helper functions
'''

from unittest import TestCase
from unittest.mock import patch
from datetime import date
import requests.exceptions as re
import models.utils.crypto_helper as CryptoHelper

# Using unittest.mock.patch to mock the API responses


class TestCryptoHelper(TestCase):
    """Unit tests for crypto helper functions
    """
    def test_fetch_data_successful(self) -> None:
        with patch("requests.get") as mock_get:
            response_dict = {
                "success": True,
                "rates": {
                    "BTC": 1
                }
            }
            mock_get.return_value.json.return_value = response_dict
            result = CryptoHelper.fetch_data(
                "http://test.api.com"
            )
            assert result == response_dict

    def test_fetch_data_fail(self) -> None:
        with patch("requests.get") as mock_get:
            response_dict = {
                "success": False,
                "error": {
                    "code": 101,
                    "type": "invalid"
                }
            }
            mock_get.return_value.json.return_value = response_dict
            result = CryptoHelper.fetch_data(
                "http://test.api.com"
            )
            assert result is False

    def test_fetch_data_http_error(self) -> None:
        with patch("requests.get") as mock_get:
            mock_get.side_effect = re.HTTPError("HTTP Error")

            with self.assertRaises(Exception):
                CryptoHelper.fetch_data(
                    "http://test.api.com"
                )

    def test_fetch_data_connection_error(self) -> None:
        with patch("requests.get") as mock_get:
            mock_get.side_effect = re.ConnectionError("Connection Error")

            with self.assertRaises(Exception):
                CryptoHelper.fetch_data(
                    "http://test.api.com"
                )

    def test_fetch_Data_timeout_error(self) -> None:
        with patch("requests.get") as mock_get:
            mock_get.side_effect = re.Timeout("Timeout Error")

            with self.assertRaises(Exception):
                CryptoHelper.fetch_data(
                    "http://test.api.com"
                )

    def test_fetch_data_redirect_error(self) -> None:
        with patch("requests.get") as mock_get:
            mock_get.side_effect = re.TooManyRedirects("Redirect Error")

            with self.assertRaises(Exception):
                CryptoHelper.fetch_data(
                    "http://test.api.com"
                )

    def test_fetch_name_of_cryptos_successful(self) -> None:
        with patch("models.utils.crypto_helper.fetch_data") as mock_fetch_data:
            mock_fetch_data.return_value = {
                "success": True,
                "crypto": {
                    "BTC": {"name": "Bitcoin"},
                    "ETH": {"name": "Ethereum"}
                }
            }

            result = CryptoHelper.fetch_name_of_cryptos()
            assert result == ["BTC", "ETH"]

    def test_fetch_name_of_cryptos_fail(self) -> None:
        with patch("models.utils.crypto_helper.fetch_data") as mock_fetch_data:
            mock_fetch_data.return_value = False

            result = CryptoHelper.fetch_name_of_cryptos()
            assert result is False

    def test_get_crypto_stat_from_live_api_successful(self) -> None:
        with patch("models.utils.crypto_helper.fetch_data") as mock_fetch_data:
            mock_fetch_data.return_value = {
                "success": True,
                "rates": {
                    "BTC": {
                        "rate": 1,
                        "high": 2,
                        "low": 3,
                        "vol": 4,
                        "cap": 5,
                        "sup": 6,
                        "change": 7,
                        "change_pct": 8
                    }
                }
            }
            result = CryptoHelper.get_crypto_stat_from_live_api("BTC")
            assert result == {
                "rate": 1,
                "high": 2,
                "low": 3,
                "vol": 4,
                "cap": 5,
                "sup": 6,
                "change": 7,
                "change_pct": 8
            }

    def test_get_crypto_stat_from_live_api_false_type(self) -> None:
        with self.assertRaises(TypeError):
            CryptoHelper.get_crypto_stat_from_live_api(1)
            CryptoHelper.get_crypto_stat_from_live_api([1])
            CryptoHelper.get_crypto_stat_from_live_api([{1: "BTC"}])

    def test_get_crypto_stat_from_live_api_fail(self) -> None:
        with patch("models.utils.crypto_helper.fetch_data") as mock_fetch_data:
            mock_fetch_data.return_value = False

            result = CryptoHelper.get_crypto_stat_from_live_api("BTC")
            assert result is False

    def test_get_crypto_day_historical_data_fail(self) -> None:
        with patch("models.utils.crypto_helper.fetch_data") as mock_fetch_data:
            mock_fetch_data.return_value = False

            result = CryptoHelper.get_crypto_day_historical_data("BTC")
            assert result is False

    def test_get_crypto_day_historical_data_false_type(self) -> None:
        with self.assertRaises(TypeError):
            CryptoHelper.get_crypto_day_historical_data(1)
            CryptoHelper.get_crypto_day_historical_data([1])
            CryptoHelper.get_crypto_day_historical_data([{1: "BTC"}])

    def test_get_crypto_day_historical_data_successful(self) -> None:
        with patch("models.utils.crypto_helper.fetch_data") as \
                mock_fetch_data, patch("datetime.date") as mock_date:
            # mock date to a fixed date
            mock_date.today.return_value = date(2023, 11, 30)
            # side effect to return different data each call
            mock_fetch_data.side_effect = [
                {
                    "success": True,
                    "date": "2023-11-30",
                    "rates": {
                        "BTC": 1
                        }
                },
                {
                    "success": True,
                    "date": "2023-11-29",
                    "rates": {
                        "BTC": 2
                        }
                }
            ]

            result = CryptoHelper.get_crypto_day_historical_data("BTC", 2)
            expected = [
                ("2023-11-29", 2),
                ("2023-11-30", 1)
            ]
            assert result == expected
