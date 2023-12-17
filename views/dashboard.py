'''
@Author:	Jiawei He(Anson)
@Date:		2023/12/1

Dashboard page for streamlit app
'''

import datetime as dt
import streamlit as st
from views.utils.views_utils import display_three_cryptos_in_one_row


def validate_crypto_list(crypto_list: list) -> None:
    """validate the crypto_list

    Args:
        crypto_list (list): list of crypto objects

    Raises:
        TypeError
        ValueError
    """

    if not isinstance(crypto_list, list):
        raise TypeError("crypto_list must be a list")
    if crypto_list == []:
        raise ValueError("crypto_list cannot be empty")


def render(crypto_list: list) -> None:
    """Entry point for the dashboard page"""

    try:
        # Validate crypto_list first before passing on
        validate_crypto_list(crypto_list)
        st.title("Cryptoeconomy Dashboard :chart_with_upwards_trend:")
        st.markdown(
            """A simple cryptocurrency dashboard to explore the cryptoeconomy"""
            """ *via [coinlayer API](https://coinlayer.com/)*"""
        )
        st.header(":rainbow[Market Overview]", divider="rainbow")
        current_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.text(f"Last updated: {current_time}")

        default = st.button("Default :house:")
        reload_button = st.button("Random :game_die:")

        # Using st.rerun to halt, make sure toggles before redenring
        if default:
            st.session_state["dashboard_display"] = "default"
            st.rerun()

        if reload_button:
            st.session_state["dashboard_display"] = "random"
            st.rerun()

        mid = len(crypto_list) // 2
        display_three_cryptos_in_one_row(crypto_list[:mid])
        display_three_cryptos_in_one_row(crypto_list[mid:])

    except (TypeError, ValueError) as e:
        st.error(e)
