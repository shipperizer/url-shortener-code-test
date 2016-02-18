.PHONY: test run install coverage migrate

PROJECT?=tiny_url
PIP?=pip
FLAKE8?=flake8
PYTEST?=py.test
PYTHON?=python


install:
	$(PIP) install -r requirements.txt

test: lint
	$(PYTEST) --cov tiny_url --cov-config .coveragerc test/

lint:
	$(FLAKE8) --config=.flake8rc tiny_url/

migrate:
	$(PYTHON) application.py db upgrade

develop:
	$(PYTHON) application.py runserver
