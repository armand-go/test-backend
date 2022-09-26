include .env
export

####################
# Setup tasks	   #
####################
install_dev:
	pip install -e ".[dev]"

install_ci:
	pip install -e ".[ci]"

install:
	pip install .

setup_venv:
		python3.10 -m venv venv


setup_dev: setup_venv
	(\
		. venv/bin/activate;\
		pip install -e ".[dev]";\
	)

setup: setup_venv
	(\
		. venv/bin/activate;\
		pip install .;\
	)


####################
# Migration   	   #
####################
migrate:
	yoyo apply

rollback:
	yoyo rollback

reset_db:
	yoyo rollback --all
	yoyo apply

list_migrations:
	yoyo list

####################
# Testing   	   #
####################
test:
	pytest -vvv -x tests

test-no-integ:
	pytest -vvv -x --ignore=tests/integration tests/

test-integ-only:
	pytest -vvv -x tests/integration

lint:
	flake8 boy.py app
	mypy --install-types --non-interactive boy.py app

cover:
	coverage run --source=app,v2 -m pytest --ignore=tests/integration -xv tests

coverage-report: cover
	coverage report -m --skip-empty

coverage-gutter: cover
	coverage html --skip-empty -d coverage
	coverage xml --skip-empty

bandit:
	bandit -r app boy.py

bandit-ci:
	bandit -r -ll -ii app boy.py

test-all: lint test bandit

run:
	python boy.py