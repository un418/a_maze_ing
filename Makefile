.PHONY: install run debug build clean fclean lint lint-strict lint-flake8 lint-mypy lint-mypy-strict test test-one

PYTHON      := poetry run python3
MAIN        := a_maze_ing.py
CONFIG      ?= config.txt
MYPY_FLAGS  := --warn-return-any --warn-unused-ignores --ignore-missing-imports \
               --disallow-untyped-defs --check-untyped-defs
PACKAGE     := mazegen
# Output file to analyze, read from OUTPUT_FILE in $(CONFIG)
OUTPUT      = $(shell sed -n 's/^OUTPUT_FILE=//p' $(CONFIG))

install:
	poetry install

run: install
	$(PYTHON) $(MAIN) $(CONFIG)

debug: install
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

# Runs + analyzes each test config
# TODO: display issues (render output gets mixed up), to be fixed later
test:
	@$(MAKE) --no-print-directory test-one CONFIG=tests/perfect-config.txt
	@$(MAKE) --no-print-directory test-one CONFIG=tests/imperfect-config.txt

# Note: the analyzer exits 0 even on a bad verdict -> read the "Verdict:" line
# Note: the solution path in the footer is not checked
test-one: run
	$(PYTHON) tests/maze_analyzer.py $(OUTPUT)

# -k (keep going): run mypy even if flake8 fails, but still exit with an error
lint:
	@echo "##### Linting #####"
	@$(MAKE) --no-print-directory -k lint-flake8 lint-mypy

# -k (keep going): run mypy even if flake8 fails, but still exit with an error
lint-strict:
	@echo "##### Linting (strict) #####"
	@$(MAKE) --no-print-directory -k lint-flake8 lint-mypy-strict

lint-flake8:
	@echo "### Flake8 ###"
	@poetry run flake8 .

lint-mypy:
	@echo "### Mypy ###"
	@poetry run mypy . $(MYPY_FLAGS)

lint-mypy-strict:
	@echo "### Mypy (strict) ###"
	@poetry run mypy . --strict

build:
	poetry build -f wheel -o .

clean:
	@echo "##### Cleaning #####"
	@echo "### Pycache ###"
	@find . -type d -name __pycache__ -prune -print -exec rm -rf {} +
	@echo "### Mypy cache ###"
	@find . -type d -name .mypy_cache -prune -print -exec rm -rf {} +
	@echo "### Generated mazes ###"
	@find . -type f -name '*maze.txt' -print -exec rm -f {} +

fclean: clean
	@echo "### Build artifacts ###"
	@rm -fv $(PACKAGE)-*
