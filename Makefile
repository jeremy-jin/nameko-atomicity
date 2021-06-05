MODULE_NAME = nameko_atomicity
.PHONY: test
SHELL = /bin/bash

test:
	@py.test test -x -vv $(ARGS)

coverage:
	flake8 $(MODULE_NAME) test
	black --check nameko_atomicity test
	coverage run --concurrency=eventlet --source $(MODULE_NAME) -m pytest test $(ARGS)
	coverage report -m

format-code:
	black nameko_atomicity test
