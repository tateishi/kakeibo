import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import typer

from kakeibo import helper

count_desc_app = typer.Typer()


HEADER_RE: re.Pattern[str] = re.compile(
    r"""
    ^
    (?P<date>\d{4}[/-]\d{2}[/-]\d{2})       # 日付
    (?:=(?P<effective_date>\d{4}[/-]\d{2}[/-]\d{2}))?  # 日付２
    \s+
    (?P<state>[*!])?                        # 状態フラグ
    \s*
    (?:\((?P<code>[^)]+)\)\s+)?             # コード
    (?P<description>[^;]+?)                 # 説明/支払先
    (?:\s*;\s*(?P<comment>.*))?             # コメント
    $
    """,
    re.VERBOSE,
)


def parse_description(text: str, pattern: re.Pattern[str] = HEADER_RE) -> str | None:
    if (m := pattern.match(text)) is None:
        return None

    return m.group("description") or None


def counter(text: str, pattern: re.Pattern[str] = HEADER_RE) -> dict[str, int]:
    counts = defaultdict(int)
    for line in text.splitlines():
        if desc := parse_description(line, pattern):
            counts[desc] += 1
    return counts


def count_file(path: Path, pattern: re.Pattern[str] = HEADER_RE) -> dict[str, int]:
    text = path.read_text()
    return counter(text, pattern)


@count_desc_app.command()
def description(path: Path):
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
        result = dict(sorted(total.items(), key=lambda item: (-item[1], item[0])))
        print(f"{json.dumps(result, ensure_ascii=False, indent=2)}")
        return

    raise typer.BadParameter(f"{path}はファイルでもディレクトリでもありません")
