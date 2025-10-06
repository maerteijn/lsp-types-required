.PHONY: install lint format

default: install

install:
	uv sync --extra dev

lint:
	uv run zmypy src
	uv run ruff check

format:
	uv run ruff check --fix
	uv run ruff format
