fmt:
    uv run ruff check . --fix
    uv run ruff format .

lint:
    uv run ruff check .

test:
    uv run pytest

all:
    just fmt
    just test
