.PHONY: install format lint test check run

install:
	poetry install --with dev

format:
	poetry run black .
	poetry run isort .

lint:
	poetry run flake8 .

test:
	poetry run pytest

check: format lint test

run:
	poetry run python hordeRL.py --log DEBUG --terminal_log

