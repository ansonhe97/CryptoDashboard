'''
@Author:	Jiawei He(Anson)
@Date:		2023/11/23

Crypto Helper functions such as fetch data from API, and parse data from API
to feed into Crypto class
'''

import datetime as dt
import requests


# Define API endpoints and API key
API_KEY = "REPLACE_WITH_YOUR_API_KEY"
LIST_ENDPOINT = "http://api.coinlayer.com/list?access_key={api_key}"
LIVE_DATA = "http://api.coinlayer.com/live?access_key={api_key}&symbols={symbol}&expand=1"
HISTORICAL_DATE = "http://api.coinlayer.com/{date}?access_key={api_key}&symbols={symbol}"
DAY_OF_WEEK = 7


def fetch_data(api_url: str) -> dict or bool:
    """Helper function to fetch data from API

    Args:
        api_url (str): The API url to fetch data from

    Raises:
        f: HTTPErrors, ConnectionErrors, TimeoutErrors, TooManyRedirects

    Returns:
        dict or bool: The data from API in json format converted to dict
        or False if the data is not fetched successfully
    """

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data["success"] is True:
            return data

        # API ONLY debugging purpose
        if data.get("error"):
            print("FETCH ERROR TYPE: ", data["error"]["type"])
        return False
    except requests.exceptions.HTTPError as http_err:
        raise f"HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError as conn_err:
        raise f"Connection error occurred: {conn_err}"
    except requests.exceptions.Timeout as timeout_err:
        raise f"Timeout error occurred: {timeout_err}"
    except requests.exceptions.TooManyRedirects as redirect_err:
        raise f"Redirect error occurred: {redirect_err}"


def fetch_name_of_cryptos() -> list:
    """Parse the data from API to get the list of crypto names

    Returns:
        list: a list of crypto names
    """

    crypto_name_list = []
    raw_data = fetch_data(LIST_ENDPOINT.format(api_key=API_KEY))
    if not raw_data:
        return False

    for symbol in raw_data["crypto"].keys():
        crypto_name_list.append(symbol)
    return crypto_name_list


def get_crypto_stat_from_live_api(symbol: str) -> dict or bool:
    """Parse data from API to get the crypto stats, and used to feed to create
    Crypto instance

    Args:
        symbol (str): The symbol of the crypto, i.e., BTC
    Returns:
        dict or bool: The crypto stat in dict format or False if the data is
        not fetched
    """

    if not isinstance(symbol, str):
        raise TypeError("symbol must be a string")

    raw_data = fetch_data(
        LIVE_DATA.format(api_key=API_KEY, symbol=symbol)
    )
    if not raw_data:
        return False
    crypto_stat = {}
    crypto_stat["rate"] = raw_data["rates"][symbol]["rate"]
    crypto_stat["high"] = raw_data["rates"][symbol]["high"]
    crypto_stat["low"] = raw_data["rates"][symbol]["low"]
    crypto_stat["vol"] = raw_data["rates"][symbol]["vol"]
    crypto_stat["cap"] = raw_data["rates"][symbol]["cap"]
    crypto_stat["sup"] = raw_data["rates"][symbol]["sup"]
    crypto_stat["change"] = raw_data["rates"][symbol]["change"]
    crypto_stat["change_pct"] = raw_data["rates"][symbol]["change_pct"]
    return crypto_stat


def get_crypto_day_historical_data(
    symbol: str,
    time_day: int = DAY_OF_WEEK
) -> list or bool:
    """Parse data from API to get the crypto historical data for a given symbol
    which is used to feed to create Crypto instance

    Args:
        symbol (str): Crypto symbol, i.e., BTC
        time_day (int, optional): The days of data needed.
        Defaults to DAY_OF_WEEK.

    Returns:
        list or bool: The crypto historical data in list format or False if
        the data is not fetched
    """

    if not isinstance(symbol, str):
        raise TypeError("symbol must be a string")
    if not isinstance(time_day, int):
        raise TypeError("time_day must be an integer")

    historical_data = []
    for day in range(time_day):
        each_date = (
            (dt.date.today() - dt.timedelta(days=day)).strftime("%Y-%m-%d")
        )
        historical_url = (
            HISTORICAL_DATE.format(
                date=each_date,
                api_key=API_KEY,
                symbol=symbol
            )
        )
        # print(historical_url)
        raw_data = fetch_data(historical_url)
        if not raw_data:
            return False

        data_set = each_date, raw_data["rates"].get(symbol, 0)
        historical_data.append(data_set)
        # Reverse the list so [oldest ... latest]
    historical_data.reverse()
    # print(historical_data)
    return historical_data
