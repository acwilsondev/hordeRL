.PHONY: install format lint test radon check run

install:
	poetry install --with dev

format:
	poetry run black .
	poetry run isort --profile=black .

test:
	poetry run pytest

radon:
	poetry run radon cc .
	poetry run radon mi .
	poetry run radon raw .
check: format lint test radon

debug:
	poetry run python hordeRL.py --log DEBUG --terminal_log

run:
	poetry run python hordeRL.py --terminal_log