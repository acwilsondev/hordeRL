.PHONY: install format lint test radon check run

install:
	poetry install --with dev

format:
	poetry run black --line-length 80 -- .
	poetry run isort .

lint:
	poetry run flake8 .

test:
	poetry run pytest

radon:
	poetry run radon cc .
	poetry run radon mi .
	poetry run radon raw .
check: format lint test radon

run:
	poetry run python hordeRL.py --log DEBUG --terminal_log

