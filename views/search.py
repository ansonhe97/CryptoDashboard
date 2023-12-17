'''
@Author:	Jiawei He(Anson)
@Date:		2023/11/25

Search page for streamlit app
'''


import streamlit as st
from views.utils.views_utils import display_one_crypto_stat
from models.crypto import Crypto
from models.crypto_name_list import CryptoNameList


def validate_crypto_name_instance(
    crypto_name_instance: CryptoNameList
) -> None:
    """validate the crypto_name_instance

    Args:
        crypto_name_instance (CryptoNameList): crypto name list object

    Raises:
        TypeError
        ValueError
    """

    if not isinstance(crypto_name_instance, CryptoNameList):
        raise TypeError("crypto_name_instance must be a CryptoNameList")
    if crypto_name_instance.name_list == []:
        raise ValueError("crypto_name_instance cannot be empty")


def render(crypto_name_instance: CryptoNameList) -> None:
    """Entry point for the search page"""

    try:
        # Validate crypto_name_instance first before passing on
        validate_crypto_name_instance(crypto_name_instance)
        st.title("Explore the Cryptoeconomy! :money_with_wings:")
        # Using selectbox property to make sure no invalid entries are
        # passed beyond this point
        crypto_search = st.selectbox(
            "Enter a crypto symbol:",
            options=crypto_name_instance.name_list,
            help="i.e, BTC, ETH, DOGE and etc.",
            placeholder="Search for an asset",
            index=None
        )
        search_button = st.button("SEARCH", type="primary")

        # Check if the user has chose a crypto from selectbox and store
        # to session state
        if crypto_search is not None and search_button:
            st.session_state["selected_crypto"] = crypto_search

    except (TypeError, ValueError) as e:
        st.error(e)


def display_searched_crypto(crypto: Crypto) -> None:
    """display the searched crypto

    Args:
        crypto (Crypto): crypto object
    """

    if not isinstance(crypto, Crypto):
        raise TypeError("crypto must be a Crypto")

    if not crypto.validate_crypto_stat():
        st.info(
            f"{crypto.symbol} has limited data from APIs, only showing rates",
            icon="ℹ️"
        )
        display_one_crypto_stat(crypto, option="missing_data")
    else:
        display_one_crypto_stat(crypto)
