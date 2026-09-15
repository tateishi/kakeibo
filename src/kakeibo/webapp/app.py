import streamlit as st
from kakeibo.webapp import contents, helper, services

def app():
    title = "Hello World!"
    st.set_page_config(layout="wide", page_title=title)

    try:
        services.load_journals()
    except subprocess.CalledProcessError as e:
        st.text(f"return code={e.returncode}, message={e.stderr}")
        return

    tabdefs = [
        helper.Tabdef(title="チェックリスト", render_func=contents.render_check_list),
        helper.Tabdef(title="立替・未払確認", render_func=contents.render_tatekae),
        helper.Tabdef(title="マネックス円残高", render_func=contents.render_monex_jpy),
        helper.Tabdef(title="プリペイド残高確認", render_func=contents.render_prepaid),
        helper.Tabdef(title="残高確認", render_func=contents.render_balance),
        helper.Tabdef(title="全体", render_func=contents.render_all),
        helper.Tabdef(
            title="科目ごと",
            render_func=contents.render_by_account,
            context={"account": "資産:現金:手元現金"},
        ),
        helper.Tabdef(title="科目選択", render_func=contents.render_account),
        helper.Tabdef(title="科目と月の選択", render_func=contents.render_account_paymonth),
        helper.Tabdef(title="忠利との補正", render_func=contents.render_tadatoshi),
        helper.Tabdef(title="時系列", render_func=contents.render_time_series),
    ]

    helper.render_tabs(tabdefs)

if __name__ == "__main__":
    app()
