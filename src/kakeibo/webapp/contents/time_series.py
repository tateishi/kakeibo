import streamlit as st
import pandas as pd
import plotly.express as px


options = {
    "家計": "kakei",
    "忠利": "tadatoshi",
}

def render(title: str, ctx):
    st.header(title)

    col1, col2, col3 = st.columns(3)

    if "journal" not in st.session_state:
        st.session_state.journal = "kakei"

    with col1:
        journal = st.radio(
            "帳簿の選択",
            options.keys(),
            key="time_series_account",
        )

    value = options[journal]
    st.session_state.journal = value

    df_name = f"{value}_df"
    acc_name = f"{value}_account"

    if df_name not in st.session_state:
        return
    df = st.session_state[df_name]

    if acc_name not in st.session_state:
        return
    account = st.session_state[acc_name]

    with col2:
        keyword = st.text_input("キーワード検索", key="text_time_series")
        if keyword:
            accounts = [
                acc
                for acc
                in account
                if all((k in acc) for k in keyword.split())
            ]
        else:
            accounts = account

    with col3:
        selected = st.selectbox("科目", accounts, key="selectbox_time_series")

    df = df[df["account"]==selected]
    df = df["date amount commodity".split()]
    df = df.groupby("date").agg({
        "amount": "sum",
        "commodity": "first",
    })
    df["total"] = df["amount"].cumsum()

    #df = df.drop_duplicates(subset="date", keep="last")

    #df = df.set_index("date")
    df = df.resample("1D").ffill()

    # st.line_chart(df["total"])

    fig = px.line(
        df,
        x=df.index,
        y="total",
        title="残高"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df)
