![Mangetamain Logo](docs/images/logo.jpeg)

<h1 align="center">Mangetamain</h1>
<p align="center">
  <em>Discover recipes, analyze ingredients and nutrition, and explore clusters with an interactive Streamlit app backed by a reproducible data pipeline.</em>
</p>

<p align="center">

  <img alt="Python" src="https://img.shields.io/badge/python-3.12-blue">
  <img alt="Poetry" src="https://img.shields.io/badge/packaging-Poetry-60A5FA">
  <img alt="Streamlit" src="https://img.shields.io/badge/app-Streamlit-FF4B4B">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-ready-2496ED">
  <img alt="pre-commit" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen">
   <img alt="Docs" src="https://img.shields.io/badge/docs-Sphinx-blueviolet">
  <img alt="Code style" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</p>


## 📚 Table of Contents
- [📚 Table of Contents](#-table-of-contents)
- [🎮 Live Demo](#-live-demo)
- [🎯 Objectives](#-objectives)
- [⚡ Quick Start](#-quick-start)
- [🧩 Requirements](#-requirements)
- [🐳 Optional: Install Docker and Docker Compose](#-optional-install-docker-and-docker-compose)
- [📦 Installation (Poetry)](#-installation-poetry)
- [🚀 Running the App](#-running-the-app)
- [🧪 Testing](#-testing)
- [🎨 Linting \& Formatting](#-linting--formatting)
- [📊 Data Pipeline (prepare datasets)](#-data-pipeline-prepare-datasets)
- [📘 Documentation](#-documentation)
- [❓ FAQ / Troubleshooting](#-faq--troubleshooting)


## 🎮 Live Demo
[Streamlit App](https://mangetamain.immock.com/)




## 🎯 Objectives

- **Exploratory Data Analysis (EDA)** on recipe and rating datasets: distributions, seasonality, popularity.
- **Feature engineering** (scores, aggregations, confidence intervals).
- **Modular architecture** (repositories, processors, analyzers) for a maintainable data pipeline.
- **Streamlit web application** for visualizing analyses (top recipes, distributions, durations, etc.).
- **Quality & CI/CD**: testing, linting, Dockerized environments, pre-commit hooks, and automated documentation (Sphinx).

---

## ⚡ Quick Start

Option A — with Poetry:
```commandline
poetry install
make run
```

Option B — with Docker Compose:
```commandline
docker compose up --build app
```

App URL: `http://localhost:8501`

## 🧩 Requirements
- Python >= 3.12, < 3.13
- Poetry
- Git

## 🐳 Optional: Install Docker and Docker Compose
Docker is recommended for a consistent, no-local-setup experience.

- Install Docker Desktop: `https://www.docker.com/products/docker-desktop/`
- Verify installation:
  ```commandline
  docker --version
  docker compose version
  ```

Notes:
- Docker Compose is included as `docker compose` (v2) in modern Docker Desktop.
- Allocate at least 2 CPUs and 4GB RAM for smoother model steps.

## 📦 Installation (Poetry)

1) Clone the repository:
```commandline
git clone https://github.com/Hugosh71/Projet_Mangetamain.git
cd Projet_Mangetamain
```

2) Create a project-local virtual environment and install dependencies:
```commandline
poetry config virtualenvs.in-project true
poetry env use python3.12
poetry install
```

3) Activate the environment:
- Windows PowerShell:
  ```commandline
  .\.venv\Scripts\activate.ps1
  ```
- macOS/Linux:
  ```commandline
  source .venv/bin/activate
  ```

## 🚀 Running the App

With Poetry (recommended for local development):
```commandline
make requirements
make run
```

With Docker Compose (no local Python needed):
```commandline
make docker-run
# or directly
docker compose up --build app
```

App URL: `http://localhost:8501`

## 🧪 Testing

Run tests in Docker:
```commandline
docker compose run --rm tests
```

Run tests with Poetry:
```commandline
poetry run pytest
```

Coverage alternative:
```commandline
poetry run pytest --cov=src --cov-report=term-missing --cov-report=xml
```

Make targets:
```commandline
make test       # pytest
make test-cov   # pytest + coverage
```

## 🎨 Linting & Formatting

With Docker:
```commandline
docker compose run --rm lint
```

With Poetry:
```commandline
poetry run black --check src tests
poetry run ruff check src tests
```

Auto-fix formatting:
```commandline
poetry run ruff check --fix src tests
poetry run ruff format src tests
```

## 📊 Data Pipeline (prepare datasets)

Run the end-to-end preprocessing and clustering pipeline, then upload prepared artifacts to S3:
```commandline
./scripts/run_pipeline.sh
```

Tips (Windows): run from Git Bash or WSL if your shell doesn’t support `bash` scripts.

## 📘 Documentation

Build once:
```commandline
poetry install --with dev
cd docs
poetry run sphinx-build -b html . _build/html
```

Open locally:
```commandline
python serve_docs.py
# then open the printed local URL
```

## ❓ FAQ / Troubleshooting

- The app does not start / port already in use
  - Another process might be using port 8501. Stop it or run Streamlit on a different port, e.g.: `poetry run streamlit run src/app/main.py --server.port=8502`.

- Poetry cannot find Python 3.12
  - Ensure Python 3.12 is installed and on PATH. Then run: `poetry env use python3.12` (macOS/Linux) or pass the full path to the Python executable on Windows.

- Docker command not found
  - Install Docker Desktop and restart your shell. Verify with `docker --version` and `docker compose version`.

- Tests fail with coverage threshold
  - The project enforces coverage (`fail_under = 90`). Use `poetry run pytest --maxfail=1 -q` to iterate quickly, then run coverage once fixes are in.

—

If you just want to try the app, the quickest route is Docker:
```commandline
docker compose up --build app
```
Then open `http://localhost:8501`.
