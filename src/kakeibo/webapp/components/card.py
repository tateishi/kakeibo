import streamlit as st

def card(title: str, contents: str, bgcolor: str="#222222"):
    st.markdown(
        f"""
<div style="
    background-color:{bgcolor};
    border-radius:12px;
    padding:20px;
    margin: 5px 0px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
">
    <h3 style="margin:0;">{title}</h3>
    <p style="font-size:1.4rem; font-weight:600;">{contents}</p>
</div>
""",
        unsafe_allow_html=True,
    )
