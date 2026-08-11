import pandas as pd
import streamlit as st

def balance(df: pd.DataFrame, name: str, account: str):
    today = pd.Timestamp.today().normalize()

    df = df[df["account"]==account]
    df = df[df["date"]<=today]
    bal = df["amount"].sum()

    st.markdown(
        f"""
<div style="
    background-color:#222222;
    border-radius:12px;
    padding:20px;
    margin: 5px 0px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
">
    <h3 style="margin:0;">{name}</h3>
    <p style="font-size:1.4rem; font-weight:600;">現金 残高 {bal:,} 円</p>
</div>
""",
            unsafe_allow_html=True,
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
