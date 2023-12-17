'''
@Author:	Jiawei He(Anson)
@Date:		2023/11/25

Page/views helper functions to help display data in streamlit
'''

import pandas as pd
from millify import millify
import streamlit as st
from models.crypto import Crypto


def display_one_crypto_stat(crypto: Crypto, option="default") -> None:
    """Display one crypto stat in streamlit

    Args:
        crypto (Crypto): The crypto object
        option (str, optional): whether crypto has enough stat to display.
        Defaults to "default".

    Raises:
        ValueError: If options are not default or missing_data
    """

    if not isinstance(crypto, Crypto):
        raise TypeError("crypto must be a Crypto object")

    # For handling missing data entry
    options = ["default", "missing_data"]
    if option not in options:
        raise ValueError(f"Invalid option: {option}")

    st.header(f":violet[{crypto.symbol}]", divider="rainbow")
    st.subheader("Market Stats")
    st.image(crypto.icon, width=100)

    if option == "default":
        # From API, some cryptos don't have following data
        col1, col2 = st.columns(2)
        col1.metric(
            label=f":blue[{crypto.symbol} / USD]",
            value=f"{crypto.rates:.3f}",
            delta=f"{crypto.change_pct:.2f} %"
        )
        col2.metric(
            label=":blue[HIGH / LOW]",
            value=f"{crypto.high:.3f} / {crypto.low:.3f}",
        )

        col3, col4 = st.columns(2)
        col3.metric(
            label=":blue[MARKET VOLUME(24H)]",
            value=f"{millify(crypto.vol, precision=2)}",
            help="The total value of all transactions for this crypto \
within the 24h timeframe."
        )
        col4.metric(
            label=":blue[MARKET CAP]",
            value=f"{millify(crypto.cap, precision=2)}",
            help="Market cap is calculated by multiplying the circulating \
supply of a crypto at the current price."
        )
    else:
        st.metric(
            label=f":blue[{crypto.symbol} / USD]",
            value=f"{crypto.rates:.3f}",
            delta=f"{crypto.change_pct:.2f} %"
        )

    chart_data = pd.DataFrame(
        crypto.historical_data, columns=["DATE", "CRYPTO"]
    )
    st.line_chart(chart_data, x="DATE", y="CRYPTO", color="#ffaa00")


def display_one_crypto_overview(crypto: Crypto) -> None:
    """Display one crypto overview in streamlit

    Args:
        crypto (Crypto): The crypto object
    """

    if not isinstance(crypto, Crypto):
        raise TypeError("crypto must be a Crypto object")

    st.subheader(f"{crypto.symbol}")
    st.image(crypto.icon, width=70)

    st.metric(
        label=f":blue[{crypto.symbol} / USD]",
        value=f"{crypto.rates:.3f}",
        delta=f"{crypto.change_pct:.2f} %"
    )
    st.divider()


def display_three_cryptos_in_one_row(crypto_list: list, n=3) -> None:
    """A page helper function to display three cryptos in one row

    Args:
        crypto_list (list): a list of cryptos
        n (int, optional): number of cryptos to display in a row.
        Defaults to 3.
    """

    if not isinstance(crypto_list, list):
        raise TypeError("crypto_list must be a list")
    if crypto_list == []:
        raise ValueError("crypto_list cannot be empty")
    if n % 3 != 0:
        raise ValueError("n must be a multiple of 3")

    col = st.columns(n)
    for i in range(n):
        with col[i]:
            display_one_crypto_overview(crypto_list[i])
