import subprocess
from pathlib import Path

import streamlit as st
from kakeibo.webapp import services


def render(title: str, _):
    st.header(title)
    if st.button("読み込み"):
        try:
            services.load_journals()
        except subprocess.CalledProcessError as e:
            st.text(f"return code={e.returncode}, message={e.stderr}")
            return

    if "kakei_df" in st.session_state:
        st.dataframe(st.session_state.kakei_df)
