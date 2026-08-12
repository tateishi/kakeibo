from pathlib import Path

import pandas as pd
import streamlit as st
from kakeibo import services


def wallet_balance(wallet: Path | str) -> int:
    wallet_dir = Path("~/wks/ledger/ledger_kakei/wallet").expanduser()

    wallet_file = wallet_dir / wallet
    wallet_df = services.read_wallet(wallet_file)
    return services.last_amount(wallet_df)

def ledger_balance(df: pd.DataFrame, account: str) -> int:
    today = pd.Timestamp.today().normalize()
    df = df[df["account"] == account]
    df = df[df["date"] <= today]
    return df["amount"].sum()

def card(title: str, contents: str, bgcolor: str):
    st.markdown(
        f"""
<div style="
    background-color:{bgcolor};
    border-radius:12px;
    padding:20px;
    margin: 5px 0px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
">
    <h3 style="margin:0;">{title}</h3>
    <p style="font-size:1.4rem; font-weight:600;">{contents}</p>
</div>
""",
        unsafe_allow_html==True,
    )

def balance(df: pd.DataFrame, name: str, wallet: Path | str, account: str, columns):
    w_balance = wallet_balance(wallet)
    l_balance = ledger_balance(df, account)

    if w_balance == l_balance:
        bg_color = "#004400"
    else:
        bg_color = "#440000"

    with columns[0]:
        card(
            title=name,
            contents=f"現金 残高 {w_balance:,} 円",
            bgcolor=bg_color
        )

    with columns[1]:
        card(
            title=name,
            contents=f"家計簿 残高 {l_balance:,} 円",
            bgcolor=bg_color
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
