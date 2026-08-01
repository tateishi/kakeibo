import streamlit as st

def render(title: str, _):
    st.header(title)
    if "raw_data" in st.session_state:
        st.dataframe(st.session_state.raw_data)
