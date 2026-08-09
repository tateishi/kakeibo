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

    with col_kakei:
        st.text(f"kakei={total_value(kakei_df, month)}")
        st.dataframe(kakei_df)

    with col_tadatoshi:
        st.text(f"tadatoshi={total_value(tadatoshi_df, month)}")
        st.dataframe(tadatoshi_df)
