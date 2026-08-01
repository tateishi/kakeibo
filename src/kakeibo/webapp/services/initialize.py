import streamlit as st
from kakeibo import services


def load_data():
    df = services.read_ledger()
    st.session_state.raw_data = df
    st.session_state.accounts = services.account_list(df)
