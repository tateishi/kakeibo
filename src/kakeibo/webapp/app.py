from dataclasses import dataclass, field
from typing import Any, Callable, Dict

import streamlit as st
from kakeibo import services
from kakeibo.webapp import contents

RenderFunc = Callable[[str], None]

Kwargs = Dict[str, Any]

@dataclass
class Tabdef:
    title: str
    render_func: RenderFunc
    context: Kwargs = field(default_factory=dict)

    def render(self):
        print(f"title={self.title}, context={self.context}")
        self.render_func(self.title, self.context)

def app():
    title = "Hello World!"
    st.set_page_config(layout="wide", page_title=title)

    st.session_state.raw_data = services.read_ledger()

    tabdefs = [
        Tabdef(title="全体", render_func=contents.render_all),
        Tabdef(title="科目ごと", render_func=contents.render_by_account, context={"account": "資産:現金:手元現金"})
    ]

    tabs = st.tabs([t.title for t in tabdefs])

    for tab, tabdef in zip(tabs, tabdefs):
        with tab:
            tabdef.render()



if __name__=="__main__":
    app()
