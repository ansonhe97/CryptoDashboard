'''
@Author:	Jiawei He(Anson)
@Date:		2023/11/26

Unit tests for crypto data class
'''

from unittest import TestCase
from models.crypto import Crypto


class TestCrypto(TestCase):
    """Unit tests for crypto data class
    """
    def test_crypto_init_with_no_data(self) -> None:
        test_crypto = Crypto("DOGE")
        self.assertEqual(test_crypto.symbol, "DOGE")
        # icon url is also based on the symbol
        self.assertEqual(
            test_crypto.icon,
            "https://assets.coinlayer.com/icons/DOGE.png"
        )

    def test_crypto_init_false_symbol_type(self) -> None:
        with self.assertRaises(TypeError):
            Crypto(1)

    def test_crypto_init_with_feed_in_stat(self) -> None:
        feed_in_stat = {
            "rate": 0.5,
            "high": 1,
            "low": 0.1,
            "vol": 1000,
            "cap": 100000,
            "sup": 5000,
            "change": 0.3,
            "change_pct": 21.2
        }
        test_crypto = Crypto("BTC", feed_in_stat)
        self.assertEqual(test_crypto.symbol, "BTC")
        self.assertEqual(test_crypto.rates, 0.5)
        self.assertEqual(test_crypto.high, 1)
        self.assertEqual(test_crypto.low, 0.1)
        self.assertEqual(test_crypto.vol, 1000)
        self.assertEqual(test_crypto.cap, 100000)
        self.assertEqual(test_crypto.sup, 5000)
        self.assertEqual(test_crypto.change, 0.3)
        self.assertEqual(test_crypto.change_pct, 21.2)
        self.assertEqual(
            test_crypto.icon,
            "https://assets.coinlayer.com/icons/BTC.png"
        )

    def test_crypto_init_with_feed_in_historical_data(self) -> None:
        feed_in_historical_data = [
            ("2023/11/21", 0.5),
            ("2023/11/22", 0.6),
            ("2023/11/23", 0.7)
        ]
        test_crypto = Crypto("BTC", historical_data=feed_in_historical_data)
        self.assertEqual(test_crypto.symbol, "BTC")
        self.assertEqual(
            test_crypto.historical_data,
            feed_in_historical_data
        )

    def test_crypto_validate_crypto_stat(self) -> None:
        feed_in_stat = {
            "rate": 0.5,
            "high": 1,
            "low": 0.1,
            "vol": 1000,
            "cap": 100000,
            "sup": 5000,
            "change": 0.3,
            "change_pct": 21.2
        }
        test_crypto = Crypto("BTC", feed_in_stat)
        self.assertTrue(test_crypto.validate_crypto_stat())

    def test_crypto_validate_crypto_stat_false(self) -> None:
        feed_in_stat = {
            "rate": 0.5,
        }
        test_crypto = Crypto("BTC", feed_in_stat)
        self.assertFalse(test_crypto.validate_crypto_stat())

    def test_crypto_str_no_data(self) -> None:
        test_crypto = Crypto("DOGE")
        self.assertEqual(
            str(test_crypto),
            "DOGE | https://assets.coinlayer.com/icons/DOGE.png | 0 | 0 | \
0 | 0 | 0 | 0 | 0 | 0 | []"
        )

    def test_crypto_str_with_data(self) -> None:
        feed_in_stat = {
            "rate": 0.5,
            "high": 1,
            "low": 0.1,
            "vol": 1000,
            "cap": 100000,
            "sup": 5000,
            "change": 0.3,
            "change_pct": 21.2
        }
        feed_in_historical_data = [
            ("2023/11/21", 0.5),
            ("2023/11/22", 0.6),
            ("2023/11/23", 0.7)
        ]
        test_crypto = Crypto(
            "BTC",
            feed_in_stat,
            feed_in_historical_data
        )
        self.assertEqual(
            str(test_crypto),
            "BTC | https://assets.coinlayer.com/icons/BTC.png | 0.5 | 1 | \
0.1 | 1000 | 100000 | 5000 | 0.3 | 21.2 | [('2023/11/21', 0.5), \
('2023/11/22', 0.6), ('2023/11/23', 0.7)]"
        )
