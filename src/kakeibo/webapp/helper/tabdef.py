from collections.abc import Callable
from dataclasses import dataclass

import streamlit as st


@dataclass
class Tabdef:
    title: str
    render_func: Callable
    context: dict | None = None

    def render(self):
        if self.context is None:
            self.render_func(self.title)
        else:
            self.render_func(self.title, self.context)


def render_tabs(tabdefs: list[Tabdef]):
    tabs = st.tabs([t.title for t in tabdefs])

    for tab, tabdef in zip(tabs, tabdefs, strict=True):
        with tab:
            tabdef.render()
