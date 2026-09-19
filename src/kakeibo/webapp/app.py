import streamlit as st
from kakeibo.webapp import contents, helper, services

def app():
    title = "家計簿"
    st.set_page_config(layout="wide", page_title=title)

    try:
        services.load_journals()
    except subprocess.CalledProcessError as e:
        st.text(f"return code={e.returncode}, message={e.stderr}")
        return

    helper.render_tabs(helper.tabdefs)

if __name__ == "__main__":
    app()
