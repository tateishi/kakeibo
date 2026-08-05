import streamlit as st
import pandas as pd

options = {
    "家計": "kakei",
    "忠利": "tadatoshi",
}

def render(title: str, ctx):
    st.header(title)

    if "journal" not in st.session_state:
        st.session_state.journal = "kakei"

    journal = st.radio(
        "帳簿の選択",
        options.keys(),
        key="journal_all",
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

    acc = account[0]
    st.write(acc)
    df = df[df["account"]==acc]
    st.dataframe(df)


def render_account(title: str, _):
    st.header(title)
    if "journal" not in st.session_state:
        st.session_state.journal = "kakei"

    journal = st.radio(
        "帳簿の選択",
        options.keys(),
        key="journal_account",
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

    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("キーワード検索")
        if keyword:
            accounts = [acc
                        for acc
                        in account
                        if all(k in acc for k in keyword.split())]
        else:
            accounts = account

    with col2:
        selected = st.selectbox("科目", accounts)

    df = df["date payee account amount commodity pay_month shop school label".split()]
    df = df[df["account"]==selected]
    df["total"] = df["amount"].cumsum()
    st.dataframe(df)


def render_account_paymonth(title: str, _):
    st.header(title)
    if "journal" not in st.session_state:
        st.session_state.journal = "kakei"

    journal = st.radio(
        "帳簿の選択",
        options.keys(),
        key="journal_paymonth",
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

    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("キーワード検索", key="keyword")
        if keyword:
            accounts = [acc
                        for acc
                        in account
                        if all(k in acc for k in keyword.split())]
        else:
            accounts = account

    with col2:
        selected = st.selectbox("科目", accounts, key="account")

    month = st.date_input("paymonth", key="month")
    month = month.strftime("%Y-%m")

    df = df["date payee account amount commodity pay_month shop school label".split()]
    df = df[df["account"]==selected]
    df = df[df["pay_month"]==month]

    df["total"] = df["amount"].cumsum()
    st.dataframe(df)
