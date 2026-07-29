import streamlit as st


def app():
    title = "Hello World!"
    st.set_page_config(layout="wide", page_title=title)

    st.header(title)

if __name__=="__main__":
    app()
