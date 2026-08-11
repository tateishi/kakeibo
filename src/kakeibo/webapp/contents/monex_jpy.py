import pandas as pd
import streamlit as st

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

    st.markdown(f"""
<div style="
    background-color:#222222;
    padding:20px;
    border-radius:12px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
">
    <h3 style="margin:0;">📊 今日までの集計</h3>
    <p style="font-size:1.4rem; font-weight:600;">マネックス証券 円残高 {total:,} 円</p>
</div>
""", unsafe_allow_html=True)

    st.dataframe(df)
