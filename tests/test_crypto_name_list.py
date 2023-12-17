'''
@Author:	Jiawei He(Anson)
@Date:		2023/11/26

Unit tests for crypto data class
'''

from unittest import TestCase
from models.crypto_name_list import CryptoNameList


class TestCryptoNameList(TestCase):
    """unit tests for crypto name list class
    """
    def test_init(self) -> None:
        test_crypto_names = ["BTC", "ETH", "DOGE"]
        crypto_name_list = CryptoNameList(test_crypto_names)
        self.assertEqual(crypto_name_list.name_list, test_crypto_names)

    def test_init_invalid_datatype(self) -> None:
        test_crypto_names = "BTC"
        with self.assertRaises(TypeError):
            CryptoNameList(test_crypto_names)

    def test_init_invalid_value(self) -> None:
        test_crypto_names = []
        with self.assertRaises(ValueError):
            CryptoNameList(test_crypto_names)

    def test_count_crypto_names(self) -> None:
        test_crypto_names = ["BTC", "ETH", "DOGE"]
        crypto_name_list = CryptoNameList(test_crypto_names)
        self.assertEqual(crypto_name_list.count_crypto_names(), 3)
