import pandas as pd
import streamlit as st

from kakeibo.webapp import components

def render(title: str, ctx):
    st.header(title)

    if not "kakei_df" in st.session_state:
        return

    accounts = [
        "資産:証券:マネックス証券:MRF",
        "資産:米国株:預り金:日本円",
    ]

    df = st.session_state.kakei_df
    df = df[df["account"].isin(accounts)]
    df["total"] = df["amount"].cumsum()

    dt = st.date_input("日付", key="monex_date")
    dt = pd.Timestamp(dt)
    total = df.loc[df["date"] <= dt, "amount"].sum()

    components.card(
        title=f"📊 {dt:%Y年%m月%d日}までの集計",
        contents=f"マネックス証券 円残高 {total:,} 円",
    )

    st.dataframe(df)
