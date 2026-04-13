.PHONY: venv install run debug clean lint build

PYTHON := python3
VENV := .venv
VENV_BIN := $(VENV)/bin
MAIN := main.py
INSTALL := $(VENV)/.install_done

all: run

$(INSTALL): requirements.txt
	@echo "Installing dependencies..."
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt
	@touch $(INSTALL)

run: install
	@echo "Running the project..."
	$(VENV_BIN)/python $(MAIN)

venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV); \
	fi

install: venv $(INSTALL)

test: install
	$(VENV_BIN)/python test/main.py

debug: install
	@echo "Running in debug mode..."
	$(VENV_BIN)/python -m pdb $(MAIN)

clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

fclean: clean
	find . -type d -name ".venv" -exec rm -r {} +

lint: install
	@echo "Running lint checks..."
	-$(VENV_BIN)/flake8 $(MAIN) src
	$(VENV_BIN)/mypy $(MAIN) src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

build: venv $(PACKAGE)
