#################################################################################
# GLOBALS                                                                       #
#################################################################################

SHELL := bash
.ONESHELL:

PROJECT_NAME     := mangetamain
PYTHON_VERSION   := 3.12
PYTHON_INTERPRETER := python
POETRY           := poetry

SRC_DIR          := src
TEST_DIR         := tests
APP_ENTRY        := $(SRC_DIR)/app/main.py

IMAGE_NAME       := $(PROJECT_NAME)
IMAGE_TAG        := latest
REGISTRY         ?=

DOCKER_COMPOSE   := docker compose
RUFF            := $(POETRY) run ruff
BLACK			:= $(POETRY) run black
FLAKE8          := $(POETRY) run flake8
PYTEST          := $(POETRY) run pytest
STREAMLIT       := $(POETRY) run streamlit

#################################################################################
# ENV & DEPENDENCIES                                                            #
#################################################################################

## Create local poetry environment
.PHONY: create-env
create-env:
	$(POETRY) env use $(PYTHON_VERSION)
	@echo ">>> Poetry environment created."
	@echo "Activate with: poetry shell"
	@echo "Or run commands with: poetry run <command>"

## Install Python dependencies
.PHONY: requirements
requirements:
	$(POETRY) install

## Install dev dependencies
.PHONY: requirements-dev
requirements-dev:
	$(POETRY) install --with dev

## Install all optional extras
.PHONY: requirements-all
requirements-all:
	$(POETRY) install --all-extras

#################################################################################
# CODE QUALITY                                                                  #
#################################################################################

## Clean Python cache files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint source and tests
.PHONY: lint
lint:
	$(BLACK) --check $(SRC_DIR) $(TEST_DIR) && $(RUFF) check $(SRC_DIR) $(TEST_DIR)

## Format code (fix lint + format)
.PHONY: format
format:
	$(RUFF) check --fix $(SRC_DIR) $(TEST_DIR)
	$(RUFF) format $(SRC_DIR) $(TEST_DIR)

## Run pre-commit hooks
.PHONY: pre-commit
pre-commit:
	$(POETRY) run pre-commit run --all-files

## Install pre-commit hooks
.PHONY: pre-commit-install
pre-commit-install:
	$(POETRY) run pre-commit install

#################################################################################
# TESTING                                                                       #
#################################################################################

## Run tests
.PHONY: test
test:
	$(PYTEST)

## Run tests with coverage
.PHONY: test-cov
test-cov:
	$(PYTEST) --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=xml

## Run specific test file (e.g. make test-file FILE=tests/unit/test_core.py)
.PHONY: test-file
test-file:
	$(PYTEST) $(FILE)

#################################################################################
# RUN APPLICATION                                                               #
#################################################################################

## Run Streamlit locally
.PHONY: run
run:
	PYTHONPATH=. $(STREAMLIT) run $(APP_ENTRY)

## Run Streamlit in dev mode (auto-reload)
.PHONY: run-dev
run-dev:
	PYTHONPATH=. $(STREAMLIT) run $(APP_ENTRY) --server.runOnSave=true

#################################################################################
# Jupyter Notebook                                                              #
#################################################################################

## Run Jupyter Notebook
.PHONY: run-notebook
run-notebook:
	PYTHONPATH=$$(pwd) $(POETRY) run jupyter lab

#################################################################################
# DOCKER                                                                       #
#################################################################################

## Build documentation
.PHONY: docs
docs:
	cd docs && poetry run sphinx-build -b html . _build/html

## Build documentation and open in browser
.PHONY: docs-serve
docs-serve: docs
	cd docs/_build/html && python -m http.server 8000

## Clean documentation build
.PHONY: docs-clean
docs-clean:
	rm -rf docs/_build

## Build Docker image
.PHONY: docker-build
docker-build:
	docker --platform linux/amd64 build -t $(IMAGE_NAME):$(IMAGE_TAG) .

## Tag Docker image (REGISTRY must be set)
.PHONY: docker-tag
docker-tag:
	@test -n "$(REGISTRY)" || (echo "REGISTRY is required" && exit 1)
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

## Push image to registry
.PHONY: docker-push
docker-push:
	@test -n "$(REGISTRY)" || (echo "REGISTRY is required" && exit 1)
	docker push $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

## Run app with Docker Compose
.PHONY: docker-run
docker-run:
	$(DOCKER_COMPOSE) up app

## Run lint inside Docker
.PHONY: docker-lint
docker-lint:
	$(DOCKER_COMPOSE) run --rm lint

## Run tests inside Docker
.PHONY: docker-test
docker-test:
	$(DOCKER_COMPOSE) run --rm tests

#################################################################################
# META                                                                          #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys
lines = sys.stdin.read()
matches = re.findall(r'^## (.+)\n\.PHONY: ([\w-]+)', lines, flags=re.M)
print("Available commands:\n")
for desc, target in matches:
    print(f"{target:25} {desc}")
endef
export PRINT_HELP_PYSCRIPT

## Show this help
.PHONY: help
help:
	@$(PYTHON_INTERPRETER) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

## Run lint, tests, and build image (common pipeline)
.PHONY: build
build: lint test docker-build
	@echo ">>> Build successful."
