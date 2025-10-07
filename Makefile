#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = mangetamain
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python
IMAGE_NAME = mangetamain
IMAGE_TAG = latest
REGISTRY ?=

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python dependencies
.PHONY: requirements
requirements:
	poetry install




## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	docker compose run --rm lint

## Format source code with ruff
.PHONY: format
format:
	ruff check --fix
	ruff format



## Run tests
.PHONY: test
test:
	docker compose run --rm tests

.PHONY: pre-commit
pre-commit:
	poetry run pre-commit run --all-files


## Run Streamlit locally (uses Poetry env if available)
.PHONY: run
run:
	poetry run streamlit run src/app/main.py --server.port=8501 --server.address=0.0.0.0

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
