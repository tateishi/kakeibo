import decimal
from datetime import date

import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta


def filter_accounts(
    df: pd.DataFrame, accounts: list[str], pay_month: date
) -> pd.DataFrame:
    month_str = pay_month.strftime("%Y-%m")
    df = df[df["account"].isin(accounts)]
    df = df[df["pay_month"] == month_str]
    df["total"] = df["amount"].cumsum()
    df = df["date payee account amount total pay_month shop".split()]
    df = df.reset_index(drop=True)

    return df


def total_value(df: pd.DataFrame, pay_month: date) -> decimal.Decimal:
    last_month = pay_month - relativedelta(months=1)

    df = df[df["date"].dt.to_period("M") == f"{last_month:%Y-%m}"]

    if len(df) == 0:
        return decimal.Decimal("0")

    return decimal.Decimal(str(df.iloc[-1]["total"]))


def render(title: str, ctx):
    st.header(title)

    if not (st.session_state.keys() >= {"kakei_df", "tadatoshi_df"}):
        return

    month = st.date_input("paymonth", key="adjust_month")

    kakei_df = filter_accounts(
        st.session_state.kakei_df,
        ["資産:立替金:立石忠利", "負債:未払金:立石忠利"],
        month,
    )

    tadatoshi_df = filter_accounts(
        st.session_state.tadatoshi_df,
        ["資産:立替金:家計", "負債:未払金:家計:忠利"],
        month,
    )

    col_kakei, col_tadatoshi = st.columns(2)

    kakei_total = total_value(kakei_df, month)
    kakei_direction = "忠利から家計" if kakei_total > 0 else "家計から忠利"

    tadatoshi_total = total_value(tadatoshi_df, month)
    tadatoshi_direction = "忠利から家計" if tadatoshi_total < 0 else "家計から忠利"

    if abs(kakei_total) == abs(tadatoshi_total):
        bg_color = "#004400"
    else:
        bg_color = "#440000"

    with col_kakei:
        st.markdown(f"""
<div style="
    background-color:{bg_color};
    padding:20px;
    border-radius:12px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
">
    <h3 style="margin:0;">{kakei_direction}</h3>
    <p style="font-size:1.4rem; font-weight:600;">補正金額 {abs(kakei_total):,} 円</p>
</div>
""", unsafe_allow_html=True)

        st.dataframe(kakei_df)

    with col_tadatoshi:
        st.markdown(f"""
<div style="
    background-color:{bg_color};
    padding:20px;
    border-radius:12px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
">
    <h3 style="margin:0;">{tadatoshi_direction}</h3>
    <p style="font-size:1.4rem; font-weight:600;">補正金額 {abs(tadatoshi_total):,} 円</p>
</div>
""", unsafe_allow_html=True)

        st.dataframe(tadatoshi_df)
