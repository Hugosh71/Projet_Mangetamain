![Mangetamain Logo](docs/images/logo.jpeg)

<h1 align="center">Mangetamain</h1>
<p align="center">
  <em>Data exploration, preprocessing, and visualization of recipe & rating datasets — including a modular Streamlit web application and CI/CD pipeline.</em>
</p>

<p align="center">
  <a href="https://github.com/Hugosh71/Projet_Mangetamain/actions">
    <img alt="Build Status" src="https://img.shields.io/github/actions/workflow/status/Hugosh71/Projet_Mangetamain/<workflow>.yml?branch=<branch_ref>">
  </a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.12-blue">
  <img alt="Poetry" src="https://img.shields.io/badge/packaging-Poetry-60A5FA">
  <img alt="Streamlit" src="https://img.shields.io/badge/app-Streamlit-FF4B4B">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-ready-2496ED">
  <img alt="pre-commit" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen">
</p>

---

## Objectives

- **Exploratory Data Analysis (EDA)** on recipe and rating datasets: distributions, seasonality, popularity.
- **Feature engineering** (scores, aggregations, confidence intervals).
- **Modular architecture** (repositories, processors, analyzers) for a maintainable data pipeline.
- **Streamlit web application** for visualizing analyses (top recipes, distributions, durations, etc.).
- **Quality & CI/CD**: testing, linting, Dockerized environments, pre-commit hooks, and automated documentation (Sphinx).

---

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Installation](#installation)
- [Run the Application](#run-locally)
- [Project Structure](#project-structure)
- [Branch Log (Work Summary)](#branch-log-work-summary)
- [Collaborative Development](#collaborative-development)
- [Quality, Tests & CI](#quality--ci-workflow)
- [Sphinx Documentation](#how-to-use-the-documentation)
  
---


## Prerequisites

- Python>=3.12,<3.13
- Poetry
- Git

### Install Python 3.12

**For Windows**:

Download and install Python on your system: https://www.python.org/downloads/release/python-31210/

**For Mac**:

```commandline
brew install python@3.12
```
Test Python installed

```commandline
python3.12 --version
```

### Install Poetry (for packaging and dependency management)

Install the latest version of [Poetry](https://python-poetry.org/)

```commandline
pip3.12 install poetry
```

Test Poetry installed:
```commandline
poetry --version
```

Until now, we are always based on the native Python environment **NOT** the desired virtual environment.
Even Poetry is always run within this native Python environment.



### Install Git (for version control)

Install [Git](https://git-scm.com/downloads) and [set up it](https://docs.github.com/fr/get-started/git-basics/set-up-git)

---

## Installation

The following guidelines show how to install the project and set up a virtual environment isolated within the project folder.
### Clone the repo to your local

Clone the repository from GitHub (remote repo) to your local machine. This creates a copy of the code that you can modify locally. Your changes will take effect once you `commit` them and `push` to the remote repository (`add` files when necessary):

```commandline
cd /your/folder
git clone https://github.com/Hugosh71/Projet_Mangetamain.git
```

This clones the repo to `/your/folder/Projet_Mangetamain` with a hidden `.git` folder inside, which keeps track of everything about the code.

We don't need to redo `git init`, because the repo is already initialized (with a `.git`) when created from GitHub. Once cloned to your local machine, it's ready!

Now, you may open the repo from your code editor (VSCode).

### Set up the virtual environment

From now on, we recommend executing commands from the terminal in VS Code.  You can open a new terminal with `Terminal > New Terminal`. As a reminder, currently we are still using the native Python environment.

The pyproject.toml file contains all Poetry configurations. Inside, you can find the following lines:

```toml
requires-python = ">=3.12,<3.13"
dependencies = [
    "streamlit (>=1.49.1,<2.0.0)"
]
```

These lines specify the Python version and the dependencies used for the virtual environment.

**Create a virtual environment with specified dependencies:**

```commandline
poetry config virtualenvs.in-project true
poetry env use python3.12
poetry install
```

This creates `.venv` under your working folder. The `.venv` is an isolated environment containing own Python interpreter and its own set of dependencies (packages).

### Activate the virtual environment

**Option 1**

In VSCode, open the Command Palette (Ctrl + Shift + P or Command + Shift + P). Enter "Python" and click "Python: Select Interpreter". Then select the environment you've just created (for example, `mangetamain-py3.12`).

Reopen the terminal. If you see the (mangetamain-py3.12) prefix, the environment is **activated** from the VSCode terminal for this project.

**Option 2**

For Windows:

```commandline
.\.venv\Scripts\activate.ps1
```

For Mac:

```commandline
source .venv/bin/activate
```

If you see the (mangetamain-py3.12) prefix, the environment is **activated** from the VSCode terminal for this project.

Then you may use `pip freeze` to check whether `streamlit` is installed. If `streamlit` exist in the list of dependencies, the virtual environment is ready and we can start a local backend and web app servers later!

---

## Run locally

```commandline
make requirements
make run
```

or run via Docker Compose

```commandline
make requirements
make docker-run
```

The app will be available at `http://localhost:8501`.

---

## Project Structure
```
Projet_Mangetamain/
├─ .github/workflows/           # CI (lint, tests, Docker build)
├─ .streamlit/                  # Streamlit configuration
├─ docs/                        # Sphinx documentation
├─ notebooks/                   # Jupyter notebooks for EDA
├─ scripts/                     # Utility scripts
├─ src/
│  ├─ app/                     # Streamlit webapp code
│  ├─ mangetamain/             # Preprocessing and core
├─ tests/                      # Unit & integration tests
├─ Dockerfile / Dockerfile.test
├─ docker-compose.yml
├─ Makefile
├─ pyproject.toml
└─ README.md
```

---

# Branch Log (work summary before merging)

### feature/eda
- Exploratory Data Analysis: data cleaning, visualization, clustering, and enriched CSV exports.
- Analysis of score distributions, durations, popularity trends, and correlations.

### feature/eda_rating
- Rating-focused EDA: confidence score calculations (e.g., Wilson lower bound), weighted means.
- Enhanced CSV exports with aggregated statistics and confidence intervals.

### feature/webapp
- Streamlit Web Application: multi-page interface (Home, Top Recipes, Distributions, Durations).
- Integrated EDA outputs and repositories; added lightweight caching for performance.
- UI/UX refinements, theme integration, and removal of large unused CSV files.

### feature/modularisation_base
- Backend refactor: modular architecture using Analyzer interfaces and AnalysisResult objects.
- Creation of the rating module (RatingCleaning, RatingPreprocessing).
- Implemented caching for “top recipes” and integrated into the Streamlit home page.

### feature/preprocessing
- Added dedicated preprocessing package: cleaning and normalization pipelines.
- Included matching unit tests.

### feature/logging
- Centralized logging system using environment variables.
- Mounted log volumes in Docker; added dedicated tests for configuration validation.

### feature/docs_sphinx
- Complete Sphinx documentation setup.
- Added build/serve scripts, integrated with CI (lint, test, Docker build).
- Activated pre-commit hooks (black, isort, ruff).

### develop / main
- Integration and release branches.
- Consolidated merges from all validated feature branches.

---

## Collaborative Development

**Fetch changes from the remote repo on GitHub:**

```commandline
git fetch
```

or fetch & merge changes from the remote repo:

```commandline
git pull
```

**Commit and push changes to the remote repo:**

```commandline
# When necessary, add all modified files and prepare for next commit
git add .

# Save changes with a message
git commit -m "..."

# Push changes to the remote repo
git push
```

**Create a new branch:**

```commandline
# Create a new branch
git branch <branch-name>

# Switch to the new branch
git checkout <branch-name>
```

**Merge a branch to main:**

```commandline
git checkout main
git merge new-feature
```

If there are conflicts, Git will ask you to resolve them manually. After resolving:

```commandline
git add <file-with-conflict>
git commit -m "..."
```

After your Pull Request has been validated and merged to the main/develop branch, follow these steps to keep your local repository up to date:

**1. Switch to the main/develop branch:**
```commandline
git checkout main
```
or

```commandline
git checkout develop
```

**2. Fetch the latest changes from remote:**
```commandline
git fetch origin # or git fetch --all
```

**3. Pull the merged changes:**
```commandline
git pull origin main
```
or

```commandline
git pull origin develop
```

**4. If working on a feature branch, rebase it on the updated main/develop branch:**
```commandline
git checkout <your-feature-branch>
```

```commandline
git rebase main
```

**5. You can push your branch:**

```commandline
git push --force-with-lease origin <branch-name>
```

**6. Clean up merged branches (optional):**
```commandline
# Delete local branch that was merged
git branch -d <merged-branch-name>

# Delete remote tracking branch
git push origin --delete <merged-branch-name>
```

---

## Quality & CI Workflow

- Launch the Streamlit app locally with Docker Compose:

  ```commandline
  docker compose up app
  ```

- Run the test suite inside the dedicated container:

  ```commandline
  docker compose run --rm tests
  ```

- Execute linting & formatting checks via Docker Compose:

  ```commandline
  docker compose run --rm lint
  ```

### Pre-commit hooks

Install the hooks once dependencies are installed:

```commandline
poetry install --with dev
poetry run pre-commit install
```

Trigger all hooks manually before committing:

```commandline
poetry run pre-commit run --all-files
```
---

## How to Use the Documentation

### Build Documentation:

```commandline
# Install dependencies
poetry install --with dev

# Build documentation
cd docs
poetry run sphinx-build -b html . _build/html

# Or use the build script
python docs/build_docs.py build
```

### View Documentation:

```commandline
# Open the built HTML files
open docs/_build/html/index.html # or start docs/_build/html/index.html

# Or serve locally
python serve_docs.py
```
