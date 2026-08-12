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

    today = pd.Timestamp.today().normalize()
    total = df.loc[df["date"] <= today, "amount"].sum()

    components.card(
        title="📊 今日までの集計",
        contents=f"マネックス証券 円残高 {total:,} 円",
    )

    st.dataframe(df)
