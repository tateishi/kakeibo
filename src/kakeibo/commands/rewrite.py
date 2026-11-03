from collections.abc import Callable
from pathlib import Path
from typing import Annotated

import typer

from kakeibo import helper

rewrite_app = typer.Typer()


def write_text_mkdir(path: Path, text: str, **kwargs) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, **kwargs)


def copy_file(src: Path, dst: Path, func: Callable | None = None) -> None:
    text = src.read_text()

    if func is not None:
        text = func(text)

    write_text_mkdir(dst, text)


def rel_path(src: Path, dst: Path, root: Path) -> Path:
    return dst / src.relative_to(root)


@rewrite_app.command()
def rewrite(
    root: Path,
    dst: Annotated[Path | None, typer.Argument()] = None,
):
    if dst is None:
        dst = Path("/tmp")

    for path in helper.iter_files(root, "*.ledger"):
        dst_parh = rel_path(path, dst, root)
        copy_file(path, dst_parh)
