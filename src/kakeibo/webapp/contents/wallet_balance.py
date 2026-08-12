from pathlib import Path

import pandas as pd
import streamlit as st
from kakeibo import services
from kakeibo.webapp import components


def balance(df: pd.DataFrame, name: str, wallet: Path | str, account: str, columns):
    w_balance = services.wallet_balance(wallet)
    l_balance = services.ledger_balance(df, account)

    if w_balance == l_balance:
        bgcolor = "#004400"
    else:
        bgcolor = "#440000"

    with columns[0]:
        components.card(
            title=name,
            contents=f"現金 残高 {w_balance:,} 円",
            bgcolor=bgcolor
        )

    with columns[1]:
        components.card(
            title=name,
            contents=f"家計簿 残高 {l_balance:,} 円",
            bgcolor=bgcolor
        )


def render(title: str, ctx):
    st.header(title)

    if not (st.session_state.keys() >= {"kakei_df", "tadatoshi_df"}):
        return

    if st.button("リロード", key="wallet_balance_button"):
        st.rerun()

    cols = st.columns(2)

    kakei_param: list[tuple[str, str, str]] = [
        ("家計財布", "mother.data", "資産:現金:家計財布"),
        ("酒代財布", "liquor.data", "資産:現金:酒代財布"),
        ("手元現金", "genkin.data", "資産:現金:手元現金"),
        ("小銭", "coins.data", "資産:現金:小銭ビン"),
        ("家計資金", "kakeishikin.data", "資産:現金:家計資金"),
        ("旅行積立", "ryokou.data", "資産:現金:旅行積立"),
        ("小遣いストック", "kodukai.data", "資産:現金:こづかいストック"),
        ("へそくり", "hesokuri.data", "資産:現金:へそくり"),
        ("プレミアム現金", "premium_exchange.data", "資産:現金:プレミアム現金"),
    ]

    df = st.session_state.kakei_df
    for name, file, account in kakei_param:
        balance(df, name, file, account, cols)


    tadatoshi_param: list[tuple[str, str, str]] = [
        ("忠利財布", "tadatoshi.data", "資産:現金:財布"),
        ("忠利小遣いストック", "tadatoshi_kodukai.data", "資産:現金:忠利小遣現金"),
    ]

    df = st.session_state.tadatoshi_df
    for name, file, account in tadatoshi_param:
        balance(df, name, file, account, cols)
