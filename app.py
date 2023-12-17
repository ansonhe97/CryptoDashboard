'''
@Author:	Jiawei He(Anson)
@Date:		2023/11/27

Cryptoeconomy Dashboard

This is the driver file for running the streamlit framework.
'''


from random import choice
import streamlit as st
import requests
from views import search, dashboard
from models.crypto import Crypto
from models.crypto_name_list import CryptoNameList
from models.utils.crypto_helper import fetch_name_of_cryptos
from models.utils.crypto_helper import get_crypto_stat_from_live_api, \
    get_crypto_day_historical_data


def main() -> None:
    """Entry point for the streamlit app"""

    try:
        # Set default page config to wide
        st.set_page_config(
            layout="wide",
            page_title="Crypto Dashboard"
        )

        st.sidebar.title("Page Navigation")
        select_option = st.sidebar.radio(
            "Select to display",
            ["Dashboard", "Search"]
        )
        if select_option == "Dashboard":
            st.session_state["page"] = "dashboard"
        elif select_option == "Search":
            st.session_state["page"] = "search"

        # Creating Crypto names and store them in session state
        list_of_crypto_names = fetch_name_of_cryptos()
        crypto_name_instance = CryptoNameList(list_of_crypto_names)
        st.session_state["crypto_names"] = crypto_name_instance

        if "dashboard_display" not in st.session_state:
            st.session_state["dashboard_display"] = "default"

        # DASHBOARD PAGE
        if st.session_state["page"] == "dashboard":
            # Default dashboard page
            if st.session_state["dashboard_display"] == "default":
                crypto_list = default_dashboard_page_cryptos()
                dashboard.render(crypto_list)
            elif st.session_state["dashboard_display"] == "random":
                crypto_list = random_dashboard_page_cryptos(
                    crypto_name_instance
                )
                dashboard.render(crypto_list)

        # SEARCH PAGE
        elif st.session_state['page'] == 'search':
            search.render(st.session_state["crypto_names"])
            # Check if the user has selected a crypto from the search page
            # from the session state and create object here
            if "selected_crypto" in st.session_state:
                searched_crypto_stat = get_crypto_stat_from_live_api(
                    st.session_state["selected_crypto"])
                crypto_historical_data = get_crypto_day_historical_data(
                    st.session_state["selected_crypto"])
                searched_crypto = Crypto(
                    st.session_state["selected_crypto"],
                    searched_crypto_stat,
                    crypto_historical_data
                )
                search.display_searched_crypto(searched_crypto)

    # Error handling
    except TypeError as te:
        st.error("TypeError: ", te)
    except ValueError as ve:
        st.error("ValueError: ", ve)
    except requests.exceptions.HTTPError as http_err:
        st.error("HTTP error occurred:", http_err)
    except requests.exceptions.ConnectionError as conn_err:
        st.error("Connection error occurred:", conn_err)
    except requests.exceptions.Timeout as timeout_err:
        st.error("Timeout error occurred:", timeout_err)
    except requests.exceptions.TooManyRedirects as redirect_err:
        st.error("Redirect error occurred:", redirect_err)
    except Exception as e:  # Also catching general exceptions for debugging
        st.error("Exception: ", e)


def default_dashboard_page_cryptos() -> list:
    """Create a list of cryptos for the default dashboard page

    Returns:
        list: list of crypto objects
    """

    crypto_name_list = ["BTC", "ETH", "BNB", "XRP", "ADA", "DOGE"]
    crypto_list = []
    for crypto in crypto_name_list:
        each_crypto_data = get_crypto_stat_from_live_api(crypto)
        each_crypto = Crypto(crypto, each_crypto_data)
        crypto_list.append(each_crypto)
    return crypto_list


def random_dashboard_page_cryptos(
    crypto_name_instance: CryptoNameList
) -> list:
    """Create a list of randomly selected cryptos

    Args:
        crypto_name_instance (CryptoNameList): CryptoNameList object

    Returns:
        list: list of crypto objects
    """

    crypto_name_list = []
    crypto_list = []
    number_in_column = 3
    for i in range(number_in_column * 2):
        crypto_name_list.append(
            choice(crypto_name_instance.name_list)
        )
        random_crypto_data = get_crypto_stat_from_live_api(
            crypto_name_list[i]
        )
        random_crypto = Crypto(crypto_name_list[i], random_crypto_data)
        crypto_list.append(random_crypto)
    return crypto_list


if __name__ == "__main__":
    main()
