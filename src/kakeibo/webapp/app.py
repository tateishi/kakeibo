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
        services.load_journals()
    except subprocess.CalledProcessError as e:
        st.text(f"return code={e.returncode}, message={e.stderr}")
        return

    tabdefs = [
        Tabdef(title="チェックリスト", render_func=contents.render_check_list),
        Tabdef(title="マネックス円残高", render_func=contents.render_monex_jpy),
        Tabdef(title="プリペイド残高確認", render_func=contents.render_prepaid),
        Tabdef(title="立替・未払確認", render_func=contents.render_tatekae),
        Tabdef(title="残高確認", render_func=contents.render_balance),
        Tabdef(title="全体", render_func=contents.render_all),
        Tabdef(
            title="科目ごと",
            render_func=contents.render_by_account,
            context={"account": "資産:現金:手元現金"},
        ),
        Tabdef(title="科目選択", render_func=contents.render_account),
        Tabdef(title="科目と月の選択", render_func=contents.render_account_paymonth),
        Tabdef(title="忠利との補正", render_func=contents.render_tadatoshi),
        Tabdef(title="時系列", render_func=contents.render_time_series),
    ]

    tabs = st.tabs([t.title for t in tabdefs])

    for tab, tabdef in zip(tabs, tabdefs):
        with tab:
            tabdef.render()


if __name__ == "__main__":
    app()
