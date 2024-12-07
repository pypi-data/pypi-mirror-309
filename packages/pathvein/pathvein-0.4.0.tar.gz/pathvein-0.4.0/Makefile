format-ruff-check:
	uv run ruff format --check .

format-ruff:
	uv run ruff format .

check-ruff:
	uv run ruff check .

check-ruff-fix:
	uv run ruff check --fix .

check-mypy:
	uv run mypy pathvein

check: format-ruff-check check-ruff check-mypy

format: format-ruff

fix: check-ruff-fix

install:
	uv sync

commit:
	uv run cz commit

publish:

