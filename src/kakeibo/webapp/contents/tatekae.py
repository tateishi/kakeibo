from datetime import date

import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta
from kakeibo import services
from kakeibo.webapp import components


def _balance(df: pd.DataFrame, accounts: list[str], pay_month: date) -> tuple[int, int]:
    previous_month = pd.Timestamp(pay_month.replace(day=1) + relativedelta(days=-1))

    df = services.filter_accounts(df, accounts, pay_month)
    used_df = df[df["date"] <= previous_month]
    used_total = used_df["amount"].sum()
    paid_df = df[df["date"] > previous_month]
    paid_total = -paid_df["amount"].sum()
    return used_total, paid_total


def _render_tatekae(df:pd.DataFrame, title: str, account: str, pay_month: date):
    used, paid = _balance(
        df,
        [account],
        pay_month,
    )
    bgcolor = "#004400" if used == paid else "#440000"

    components.card(
        title=title,
        contents=f"{pay_month:%Y年%m月}<br>{used:,}<br>{paid:,}",
        bgcolor=bgcolor,
    )


def render(title: str, ctx):
    st.header(title)

    if not st.session_state.keys() >= {"kakei_df", "tadatoshi_df"}:
        return

    if st.button("リロード", key="tatekae_button"):
        st.rerun()

    ncols = 5
    cols = st.columns(ncols)
    today = date.today()
    params = [
        (st.session_state.kakei_df, "立替忠利", "資産:立替金:立石忠利"),
        (st.session_state.kakei_df, "未払忠利", "負債:未払金:立石忠利"),
        (st.session_state.tadatoshi_df, "立替家計", "資産:立替金:家計"),
        (st.session_state.tadatoshi_df, "未払家計", "負債:未払金:家計:忠利"),
    ]

    for df, title, account in params:
        for i, n in enumerate(range(-2, 3)):
            pay_month = today + relativedelta(months=n)
            with cols[i % 5]:
                _render_tatekae(
                    df,
                    title,
                    account,
                    pay_month,
                )
