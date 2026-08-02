from pathlib import Path

import streamlit as st
from kakeibo import services


def load_data(file: Path | str):
    df = services.read_ledger(file)
    st.session_state.raw_data = df
    st.session_state.accounts = services.account_list(df)
