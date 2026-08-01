test:
	pytest -q

build:
	uv build

local-install:
	uv pip install -e .

web:
	uv run kakeibo-web

run:
	uv run kakeibo
