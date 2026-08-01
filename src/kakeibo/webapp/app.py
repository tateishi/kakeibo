import streamlit as st

from kakeibo import services

def app():
    title = "Hello World!"
    st.set_page_config(layout="wide", page_title=title)

    st.header(title)

    st.session_state.raw_data = services.read_ledger()

    st.dataframe(st.session_state.raw_data)


if __name__=="__main__":
    app()
