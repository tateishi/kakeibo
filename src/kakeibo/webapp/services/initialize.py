from pathlib import Path

import streamlit as st
from kakeibo import services


def load_data(file: Path | str):
    df = services.read_ledger(file)
    st.session_state.raw_data = df
    st.session_state.accounts = services.account_list(df)

def load_journals():
    file_kakei = Path("~/wks/ledger/ledger_kakei/journal/kakei/main.ledger")
    file_tadatoshi = Path("~/wks/ledger/ledger_kakei/journal/tadatoshi/main.ledger")

    df = services.read_ledger(file_kakei)
    st.session_state.kakei_df = df
    st.session_state.kakei_account = services.account_list(df)

    df = services.read_ledger(file_tadatoshi)
    st.session_state.tadatoshi_df = df
    st.session_state.tadatoshi_account = services.account_list(df)
