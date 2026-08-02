import subprocess

import streamlit as st
from kakeibo.webapp import services


def render(title: str, _):
    st.header(title)
    if st.button("読み込み"):
        try:
            services.load_data()
        except subprocess.CalledProcessError as e:
            st.text(f"return code={e.returncode}, message={e.stderr}")
            return

    if "raw_data" in st.session_state:
        st.dataframe(st.session_state.raw_data)
