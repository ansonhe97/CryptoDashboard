'''
@Author:	Jiawei He(Anson)
@Date:		2023/11/21

Crypto data class
'''


ICON_URL = "https://assets.coinlayer.com/icons/{symbol}.png"


class Crypto:
    """The Crypto class represents a cryptocurrency

    Attributes:
        - symbol: the symbol of the crypto
        - icon: the icon url of the crypto
        - rates: the current exchange rate of the crypto
        - high: the highest rate of the crypto in the last 24 hours
        - low: the lowest rate of the crypto in the last 24 hours
        - vol: the volume of the crypto in the last 24 hours
        - cap: the market cap of the crypto
        - sup: the supply of the crypto
        - change: the change of the crypto in the last 24 hours
        - change_pct: the change percentage of the crypto in the last 24 hours

    Methods:
        - __init__: initialises a crypto instance
        - __str__: return a string representation of the crypto instance
        - validate_crypto_stat: validate the crypto_stat data for later
        display funtions
    """
    def __init__(
        self,
        symbol: str,
        crypto_stat: dict = None,
        historical_data: list = None
    ):
        if not isinstance(symbol, str):
            raise TypeError("symbol must be a string")

        self.symbol = symbol
        self.icon = ICON_URL.format(symbol=symbol)

        if crypto_stat is None:
            crypto_stat = {}
        elif not isinstance(crypto_stat, dict):
            raise TypeError("crypto_stat must be a dict")

        self.rates = crypto_stat.get("rate", 0)
        self.high = crypto_stat.get("high", 0)
        self.low = crypto_stat.get("low", 0)
        self.vol = crypto_stat.get("vol", 0)
        self.cap = crypto_stat.get("cap", 0)
        self.sup = crypto_stat.get("sup", 0)
        self.change = crypto_stat.get("change", 0)
        self.change_pct = crypto_stat.get("change_pct", 0)

        if historical_data is None:
            historical_data = []
        elif not isinstance(historical_data, list):
            raise TypeError("historical_data must be a list")

        # [(DATE, RATE), ...]
        self.historical_data = historical_data

    def __str__(self) -> str:
        """String representation of the crypto instance

        Returns:
            str: the str representation of the crypto instance
        """
        return (
            f"{self.symbol} | {self.icon} | {self.rates} | {self.high} | \
{self.low} | {self.vol} | {self.cap} | {self.sup} | {self.change} | \
{self.change_pct} | {self.historical_data}"
        )

    def validate_crypto_stat(self):
        """validate the crypto_stat data for later display funtions
        with streamlit

        Returns:
            boolean: True if the crypto has following attributes,
            False otherwise

        >>> crypto = Crypto("DOGE", {"rate": 1})
        >>> crypto.validate_crypto_stat()
        False
        >>> crypto = Crypto("DOGE", {"rate": 1, "high": 2, "low": 3, \
"vol": 4, "cap": 5, "sup": 6, "change": 7, "change_pct": 8})
        >>> crypto.validate_crypto_stat()
        True
        """

        # typical missing data from oberving the API
        attribute_list = [
            self.high,
            self.low,
            self.vol,
            self.cap,
            self.sup,
            self.change,
            self.change_pct
        ]
        for attribute in attribute_list:
            if attribute == 0:
                return False
        return True
