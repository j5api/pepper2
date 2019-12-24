.PHONY: all clean lint type test test-cov

CMD:=poetry run
PYMODULE:=pepper2
TESTS:=tests
EXTRACODE:=

all: type test lint

lint:
	$(CMD) flake8 $(PYMODULE) $(TESTS) $(EXTRACODE)

type:
	$(CMD) mypy $(PYMODULE) $(TESTS) $(EXTRACODE)

test:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS)

test-ci:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report xml

test-cov:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report html

isort:
	$(CMD) isort --recursive $(PYMODULE) $(TESTS) $(EXTRACODE)

clean:
	git clean -Xdf # Delete all files in .gitignore
