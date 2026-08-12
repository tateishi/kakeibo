import decimal
from datetime import date

import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta
from kakeibo.webapp import components
from kakeibo import services


def render(title: str, ctx):
    st.header(title)

    if not (st.session_state.keys() >= {"kakei_df", "tadatoshi_df"}):
        return

    month = st.date_input("paymonth", key="adjust_month")

    kakei_df = services.filter_accounts(
        st.session_state.kakei_df,
        ["資産:立替金:立石忠利", "負債:未払金:立石忠利"],
        month,
    )

    tadatoshi_df = services.filter_accounts(
        st.session_state.tadatoshi_df,
        ["資産:立替金:家計", "負債:未払金:家計:忠利"],
        month,
    )

    col_kakei, col_tadatoshi = st.columns(2)

    kakei_total = services.total_value(kakei_df, month)
    kakei_direction = "忠利から家計" if kakei_total > 0 else "家計から忠利"

    tadatoshi_total = services.total_value(tadatoshi_df, month)
    tadatoshi_direction = "忠利から家計" if tadatoshi_total < 0 else "家計から忠利"

    if abs(kakei_total) == abs(tadatoshi_total):
        bgcolor = "#004400"
    else:
        bgcolor = "#440000"

    with col_kakei:
        components.card(
            title=kakei_direction,
            contents=f"補正金額 {abs(kakei_total):,} 円",
            bgcolor=bgcolor,
        )
        st.dataframe(kakei_df)

    with col_tadatoshi:
        components.card(
            title=tadatoshi_direction,
            contents=f"補正金額 {abs(tadatoshi_total):,} 円",
            bgcolor=bgcolor,
        )
        st.dataframe(tadatoshi_df)
