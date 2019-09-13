include .env
export $(shell sed 's/=.*//' .env)
export FLASK_APP := myapp.py

run:
	gunicorn --reload -b :$(API_PORT) rest_api.api:api

install: install-deps install-githooks

install-deps:
	pip install -r requirements.txt

install-githooks:
	cp git-hooks/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

test-all:
	tox

test:
	tox -e python3.6.8

unit-tests:
	tox -e python3.6.8 tests/unit

functional-tests:
	tox -e python3.6.8 tests/functional

lint:
	tox -e linters

coverage:
	tox -e coverage

clean:
	rm -rf .tox

db-init:
	flask db init

db-migrate:
	flask db migrate --message "$(message)"

db-upgrade:
	flask db upgrade $(revision)

db-downgrade:
	flask db downgrade $(revision)

.PHONY: run install install-deps install-githooks test-all test unit-tests functional-tests lint coverage clean db-init db-migrate db-upgrade db-downgrade
