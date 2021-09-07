MODULE_NAME = nameko_atomicity
.PHONY: test
SHELL = /bin/bash

HTMLCOV_DIR ?= htmlcov

# test
coverage-html: test
	 coverage html -d $(HTMLCOV_DIR) --fail-under 100

coverage-report: test
	coverage report -m

lint:
	flake8 nameko_atomicity test

test:
	coverage run --concurrency=eventlet --source=nameko_atomicity -m pytest test $(ARGS)

coverage: lint coverage-html coverage-report test

format-code:
	black nameko_atomicity test
