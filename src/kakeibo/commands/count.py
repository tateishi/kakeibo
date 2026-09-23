import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import typer

from kakeibo import helper

count_app = typer.Typer()


POSTING_RE: re.Pattern[str] = re.compile(
    r"""
    ^
    (?P<indent>\s+)                         # インデント（必須）
    (?:
        ;\s*(?P<comment_only>.*)            # インデント直後のコメント行
      |
        (?P<account>\S+(?:\s\S+)*)          # アカウント（空白1つで何語でもOK）
        (?:                                 # 金額・通貨（任意）
            \s{2,}                          # 2つ以上の空白で区切り
            (?P<amount>[-+]?\d[\d,\.]*)     # 金額
            (?:\s+(?P<currency>\S+))?       # 通貨（任意）
        )?
        (?:\s*;\s*(?P<comment>.*))?         # コメント（任意）
    )
    \s*$
    """,
    re.VERBOSE,
)


def parse_acount(text: str, pattern: re.Pattern[str] = POSTING_RE) -> str | None:
    if (m := pattern.match(text)) is None:
        return None

    return m.group("account") or None


def counter(text: str, pattern: re.Pattern[str] = POSTING_RE) -> dict[str, int]:
    counts = defaultdict(int)
    for line in text.splitlines():
        if account := parse_acount(line, pattern):
            counts[account] += 1
    return counts


def count_file(path: Path, pattern: re.Pattern[str] = POSTING_RE) -> dict[str, int]:
    text = path.read_text()
    return counter(text, pattern)


@count_app.command()
def count(path: Path):
    if not path.exists():
        raise typer.BadParameter(f"{path}は存在しません")

    if path.is_file():
        print(f"{path}")
        return

    if path.is_dir():
        total = Counter()
        for file in helper.iter_files(path, "*.ledger"):
            data = count_file(file)
            total.update(data)
        print(f"{json.dumps(dict(total.most_common()), ensure_ascii=False, indent=2)}")
        return

    raise typer.BadParameter(f"{path}はファイルでもディレクトリでもありません")
