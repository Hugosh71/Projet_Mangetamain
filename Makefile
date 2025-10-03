#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = mangetamain
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python
IMAGE_NAME = mangetamain
IMAGE_TAG = latest
REGISTRY ?=
DOCKER_COMPOSE = docker compose
POETRY = poetry

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python dependencies
.PHONY: requirements
requirements:
	$(POETRY) install

## Install development dependencies
.PHONY: requirements-dev
requirements-dev:
	$(POETRY) install --with dev

## Install all optional extras
.PHONY: requirements-all
requirements-all:
	$(POETRY) install --all-extras

## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	$(DOCKER_COMPOSE) run --rm lint

## Lint locally without Docker
.PHONY: lint-local
lint-local:
	$(POETRY) run ruff check src tests

## Format source code with ruff
.PHONY: format
format:
	ruff check --fix
	ruff format

## Format locally with Poetry env
.PHONY: format-local
format-local:
	$(POETRY) run ruff check --fix src tests
	$(POETRY) run ruff format src tests

## Run tests
.PHONY: test
test:
	$(DOCKER_COMPOSE) run --rm tests

## Run tests locally
.PHONY: test-local
test-local:
	$(POETRY) run pytest

## Run tests with coverage locally
.PHONY: test-cov
test-cov:
	$(POETRY) run pytest --cov=src --cov-report=term-missing --cov-report=xml

## Run a specific test file: make test-file FILE=tests/unit/test_core.py
.PHONY: test-file
test-file:
	$(POETRY) run pytest $(FILE)

.PHONY: pre-commit
pre-commit:
	$(POETRY) run pre-commit run --all-files

## Install pre-commit hooks
.PHONY: pre-commit-install
pre-commit-install:
	$(POETRY) run pre-commit install

## Run Streamlit locally (uses Poetry env if available)
.PHONY: run
run:
	$(POETRY) run streamlit run src/app/main.py --server.port=8501 --server.address=0.0.0.0

## Run Streamlit via Docker Compose
.PHONY: run-docker
run-docker:
	$(DOCKER_COMPOSE) up app

## Run Streamlit in dev mode (auto-reload)
.PHONY: run-dev
run-dev:
	$(POETRY) run streamlit run src/app/main.py --server.port=8501 --server.address=0.0.0.0 --server.runOnSave=true

## Build Docker image
.PHONY: docker-build
docker-build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

## Run Docker container locally (http://localhost:8501)
.PHONY: docker-run
docker-run:
	docker run --rm -it -p 8501:8501 $(IMAGE_NAME):$(IMAGE_TAG)

## Tag image for a registry (set REGISTRY=aws_account_id.dkr.ecr.region.amazonaws.com)
.PHONY: docker-tag
docker-tag:
	@test -n "$(REGISTRY)" || (echo "REGISTRY is required" && exit 1)
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

## Push image to registry (requires docker login)
.PHONY: docker-push
docker-push:
	@test -n "$(REGISTRY)" || (echo "REGISTRY is required" && exit 1)
	docker push $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	poetry env use $(PYTHON_VERSION)
	@echo ">>> Poetry environment created. Activate with: "
	@echo '$$(poetry env activate)'
	@echo ">>> Or run commands with:\npoetry run <command>"

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Make dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) mangetamain/dataset.py

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
