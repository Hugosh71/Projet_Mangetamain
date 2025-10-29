# Getting Started with Development

## Prerequisites

Before starting development, ensure you have:

* Python 3.12+
* Poetry for dependency management
* Git for version control
* Docker (optional, for containerized development)

## Development Setup

1. **Clone the repository:**

```bash
git clone https://github.com/Hugosh71/Projet_Mangetamain.git
cd Projet_Mangetamain
```

1. **Set up the development environment:**

```bash
poetry config virtualenvs.in-project true
poetry env use python3.12
poetry install --with dev
```

1. **Install pre-commit hooks:**

```bash
poetry run pre-commit install
```

1. **Activate the virtual environment:**

```bash
source .venv/bin/activate  # macOS/Linux
.\.venv\Scripts\activate.ps1  # Windows
```
