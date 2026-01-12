.PHONY: install format lint test radon check run clean debug localization

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

localization:
	./scripts/check_i18n.sh

check: localization format lint test radon

debug:
	poetry run python hordeRL.py --log DEBUG --terminal_log

run:
	poetry run python hordeRL.py

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage coverage.xml \
		dist build *.egg-info \
		*.world prof.txt .log logs
