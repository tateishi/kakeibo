import subprocess
from dataclasses import dataclass, field
from typing import Any, Callable, Dict

import streamlit as st
from kakeibo.webapp import contents, services

RenderFunc = Callable[[str], None]

Kwargs = Dict[str, Any]

@dataclass
class Tabdef:
    title: str
    render_func: RenderFunc
    context: Kwargs = field(default_factory=dict)

    def render(self):
        self.render_func(self.title, self.context)

def app():
    title = "Hello World!"
    st.set_page_config(layout="wide", page_title=title)

    try:
        services.load_data()
    except subprocess.CalledProcessError as e:
        st.text(f"return code={e.returncode}, message={e.stderr}")
        return

    tabdefs = [
        Tabdef(title="全体", render_func=contents.render_all),
        Tabdef(title="科目ごと", render_func=contents.render_by_account, context={"account": "資産:現金:手元現金"}),
        Tabdef(title="科目選択", render_func=contents.render_account),
        Tabdef(title="科目と月の選択", render_func=contents.render_account_paymonth),
    ]

    tabs = st.tabs([t.title for t in tabdefs])

    for tab, tabdef in zip(tabs, tabdefs):
        with tab:
            tabdef.render()



if __name__=="__main__":
    app()
