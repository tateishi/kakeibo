import streamlit as st
import pandas as pd

def render(title: str, ctx):
    st.header(title)

    if not all((var in st.session_state) for var in ["kakei_df", "tadatoshi_df"]):
        return

    month = st.date_input("paymonth", key="adjust_month")
    month_str = month.strftime("%Y-%m")
    print(month)
    print(month_str)
    kakei_df = st.session_state.kakei_df
    tadatoshi_df = st.session_state.tadatoshi_df

    kakei_df = kakei_df[
        ((kakei_df["account"]=="資産:立替金:立石忠利") |
         (kakei_df["account"]=="負債:未払金:立石忠利")) &
        (kakei_df["pay_month"]==month_str)
    ]

    kakei_df["total"] = kakei_df["amount"].cumsum()
    kakei_df = kakei_df["date payee account amount total pay_month shop".split()]
    kakei_df = kakei_df.reset_index(drop=True)

    tadatoshi_df = tadatoshi_df[
        ((tadatoshi_df["account"]=="資産:立替金:家計") |
         (tadatoshi_df["account"]=="負債:未払金:家計:忠利")) &
        (tadatoshi_df["pay_month"]==month_str)
    ]

    tadatoshi_df["total"] = tadatoshi_df["amount"].cumsum()
    tadatoshi_df = tadatoshi_df["date payee account amount total pay_month shop".split()]
    tadatoshi_df = tadatoshi_df.reset_index(drop=True)

    col_kakei, col_tadatoshi = st.columns(2)

    with col_kakei:
        st.text("kakei")
        st.dataframe(kakei_df)

    with col_tadatoshi:
        st.text("tadatoshi")
        st.dataframe(tadatoshi_df)
