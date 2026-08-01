import streamlit as st

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
