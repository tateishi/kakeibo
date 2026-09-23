from collections.abc import Iterator
from pathlib import Path


def iter_files(root: Path, pattern: str) -> Iterator[Path]:
    yield from (p for p in root.rglob(pattern) if p.is_file())
