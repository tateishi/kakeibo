import pandas as pd
import streamlit as st
from kakeibo.webapp import components


def balance(df: pd.DataFrame, name: str, account: str):
    today = pd.Timestamp.today().normalize()

    df = df[df["account"] == account]
    df = df[df["date"] <= today]
    bal = df["amount"].sum()

    components.card(
        title=name,
        contents=f"現金 残高 {bal:,} 円",
    )


def render(title: str, ctx):
    st.header(title)

    if not (st.session_state.keys() >= {"kakei_df", "tadatoshi_df"}):
        return

    if st.button("リロード", key="prepaid_balance_button"):
        st.rerun()

    kakei_param: list[tuple[str, str]] = [
        ("かぞくのおさいふ", "資産:現金:かぞくのおさいふ"),
        ("Lu Vit", "資産:現金:LuVit"),
        ("さくらカード", "資産:現金:さくらカード"),
        ("コストコカード", "資産:現金:コストコカード"),
    ]

    df = st.session_state.kakei_df
    for name, account in kakei_param:
        balance(df, name, account)

    tadatoshi_param: list[tuple[str, str]] = [
        ("Paypay", "資産:現金:Paypay"),
        ("名古屋プレミアム商品券", "資産:現金:プレミアム商品券"),
    ]

    df = st.session_state.tadatoshi_df
    for name, account in tadatoshi_param:
        balance(df, name, account)
