![Mangetamain Logo](docs/images/logo.jpeg)

# Mangetamain

Live demo: `https://mangetamain.immock.com/`

Discover recipes, analyze ingredients and nutrition, and explore clusters with an interactive Streamlit app backed by a reproducible data pipeline.

## Table of Contents
- Quick Start
- Requirements
- Optional: Install Docker and Docker Compose
- Installation (Poetry)
- Running the App
- Testing
- Linting & Formatting
- Data Pipeline (prepare datasets)
- Documentation
- Best Practices
- FAQ / Troubleshooting

## Quick Start

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

## Requirements
- Python >= 3.12, < 3.13
- Poetry
- Git

## Optional: Install Docker and Docker Compose
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

## Installation (Poetry)

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

## Running the App

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

## Testing

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

## Linting & Formatting

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

## Data Pipeline (prepare datasets)

Run the end-to-end preprocessing and clustering pipeline, then upload prepared artifacts to S3:
```commandline
./scripts/run_pipeline.sh
```

Tips (Windows): run from Git Bash or WSL if your shell doesn’t support `bash` scripts.

## Documentation

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

## Best Practices
- Keep a clean environment: prefer Poetry or Docker; avoid mixing systems Python and project venvs.
- Re-run tests before opening a PR or sharing results.
- Use Docker when you want zero local Python setup or reproducibility across machines.
- Large data stays under `data/` locally; avoid committing private data or credentials.

## FAQ / Troubleshooting

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
