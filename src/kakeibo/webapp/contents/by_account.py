import streamlit as st
import pandas as pd


def render(title: str, ctx):
    st.header(title)
    if "raw_data" not in st.session_state:
        return

    if "account" in ctx:
        account = ctx["account"]
        st.write(account)
        df = st.session_state.raw_data
        df = df[df["account"]==account]
        st.dataframe(df)


def render_account(title: str, _):
    st.header(title)
    if "raw_data" not in st.session_state:
        return

    if "accounts" not in st.session_state:
        return

    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("キーワード検索")
        if keyword:
            accounts = [acc
                        for acc
                        in st.session_state.accounts
                        if all(k in acc for k in keyword.split())]
        else:
            accounts = st.session_state.accounts

    with col2:
        selected = st.selectbox("科目", accounts)

    df = st.session_state.raw_data
    df = df["date payee account amount commodity pay_month shop school label".split()]
    df = df[df["account"]==selected]
    df["total"] = df["amount"].cumsum()
    st.dataframe(df)
