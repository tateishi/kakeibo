from datetime import date

import pandas as pd
import streamlit as st
from kakeibo import services
from kakeibo.webapp import components
from dateutil.relativedelta import relativedelta


def check(df: pd.DataFrame, name: str, wallet: str, account: str):
    w_balance = services.wallet_balance(wallet)
    l_balance = services.ledger_balance(df, account)

    bgcolor = "#004400" if w_balance == l_balance else "#440000"

    components.card(
        title=name,
        contents=f"""
        財布: {w_balance:,}円<br>
        残高: {l_balance:,}円""",
        bgcolor=bgcolor
    )


def render_balance(df: pd.DataFrame, check_list: list[tuple[str, str, str]], columns):
    ncols = len(columns)

    for i, (name, file, account) in enumerate(check_list):
        with columns[i % ncols]:
            check(df, name, file, account)


def render_trans_month(pay_month: date):
    kakei_df = services.filter_accounts(
        st.session_state.kakei_df,
        ["資産:立替金:立石忠利", "負債:未払金:立石忠利"],
        pay_month,
    )

    tadatoshi_df = services.filter_accounts(
        st.session_state.tadatoshi_df,
        ["資産:立替金:家計", "負債:未払金:家計:忠利"],
        pay_month,
    )

    kakei_total = services.total_value(kakei_df, pay_month)
    kakei_direction = "忠利から家計" if kakei_total > 0 else "家計から忠利"

    tadatoshi_total = services.total_value(tadatoshi_df, pay_month)
    tadatoshi_direction = "忠利から家計" if tadatoshi_total < 0 else "家計から忠利"

    if abs(kakei_total) == abs(tadatoshi_total):
        bgcolor = "#004400"
    else:
        bgcolor = "#440000"

    components.card(
        title=f"補正{pay_month:%Y年%m月}",
        contents=f"""
        {kakei_direction}: {abs(kakei_total):,}円<br>
        {tadatoshi_direction}: {abs(tadatoshi_total):,}円
        """,
        bgcolor=bgcolor
    )


def render_trans(columns):
    ncols = len(columns)

    for i, n in enumerate(range(-2, 3)):
        with columns[i % ncols]:
            render_trans_month(date.today() + relativedelta(months=n))


def render_credit_card_month(df: pd.DataFrame, name: str, account: str, pay_month: date):
    df = services.filter_accounts(
        df,
        [account],
        pay_month
    )

    first_day = pd.Timestamp(pay_month.replace(day=1))

    df_used = df[df["date"] < first_day]
    used = -df_used["amount"].sum()

    df_paid = df[df["date"] >= first_day]
    paid = df_paid["amount"].sum()

    bgcolor = "#004400" if used == paid else "#440000"

    components.card(
        title=f"{name}<br>{pay_month:%Y年%m月}",
        contents=f"利用額={used:,}円<br>決済額={paid:,}円",
        bgcolor=bgcolor
    )


def render_credit_card(df: pd.DataFrame, name: str, account: str, columns):
    ncols = len(columns)

    for i, n in enumerate(range(-2, 3)):
        with columns[i % ncols]:
            render_credit_card_month(
                df,
                name,
                account,
                date.today() + relativedelta(months=n)
            )


def render(title: str, ctx):
    st.header(title)

    if not (st.session_state.keys() >= {"kakei_df", "tadatoshi_df"}):
        return

    if st.button("リロード", key="check_list_button"):
        st.rerun()

    ncols = 5

    cols = st.columns(ncols)
    check_list_kakei: list[tuple[str, str, str]] = [
        ("家計財布", "mother.data", "資産:現金:家計財布"),
        ("酒代財布", "liquor.data", "資産:現金:酒代財布"),
        ("手元現金", "genkin.data", "資産:現金:手元現金"),
        ("へそくり", "hesokuri.data", "資産:現金:へそくり"),
        ("プレミアム現金", "premium_exchange.data", "資産:現金:プレミアム現金"),
        ("小銭", "coins.data", "資産:現金:小銭ビン"),
        ("家計資金", "kakeishikin.data", "資産:現金:家計資金"),
        ("旅行積立", "ryokou.data", "資産:現金:旅行積立"),
        ("小遣いストック", "kodukai.data", "資産:現金:こづかいストック"),
    ]
    render_balance(st.session_state.kakei_df, check_list_kakei,  cols)

    cols = st.columns(ncols)
    check_list_tadatoshi: list[tuple[str, str, str]] = [
        ("忠利財布", "tadatoshi.data", "資産:現金:財布"),
        ("忠利小遣い", "tadatoshi_kodukai.data", "資産:現金:忠利小遣現金"),
    ]
    render_balance(st.session_state.tadatoshi_df, check_list_tadatoshi,  cols)

    cols = st.columns(ncols)
    render_trans(cols)

    cols = st.columns(ncols)
    render_credit_card(
        st.session_state.kakei_df,
        "ドコモカード",
        "負債:クレジット:ドコモカード6601",
        cols
    )
    render_credit_card(
        st.session_state.kakei_df,
        "アマゾン",
        "負債:クレジット:アマゾンカード",
        cols
    )
    render_credit_card(
        st.session_state.kakei_df,
        "楽天カード",
        "負債:クレジット:楽天カード",
        cols
    )
    render_credit_card(
        st.session_state.kakei_df,
        "シネマ",
        "負債:クレジット:シネマイレージ",
        cols
    )
    render_credit_card(
        st.session_state.tadatoshi_df,
        "オリーブカード",
        "負債:クレジット:オリーブカード",
        cols
    )
    render_credit_card(
        st.session_state.tadatoshi_df,
        "エクスプレス",
        "負債:クレジット:エクスプレスカード",
        cols
    )
