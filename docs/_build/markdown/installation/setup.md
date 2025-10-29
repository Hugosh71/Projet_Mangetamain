# Environment Setup

## Method 1: Using Poetry (Recommended)

This is the recommended method for development and local usage.

1. **Clone the repository:**

```bash
git clone https://github.com/Hugosh71/Projet_Mangetamain.git
cd Projet_Mangetamain
```

1. **Configure Poetry to create virtual environments in the project:**

```bash
poetry config virtualenvs.in-project true
poetry env use python3.12
```

1. **Install dependencies:**

```bash
poetry install
```

Install additional development dependencies:

```bash
poetry install --with dev
poetry run pre-commit install
```

This will install:

* Testing tools (pytest, pytest-cov)
* Code formatting (black, ruff)
* Linting (flake8, ruff)
* Pre-commit hooks

1. **Activate the virtual environment:**

   **Option A: Using VS Code**
   - Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
   - Type “Python: Select Interpreter”
   - Select the mangetamain environment

   **Option B: Using terminal**

   Windows:
   ```bash
   .\.venv\Scripts\activate.ps1
   ```

   macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```
2. **Run the application:**

```bash
poetry run streamlit run src/app/main.py --server.port=8501 --server.address=0.0.0.0
```

## Method 2: Using Docker

For containerized deployment:

1. **Clone the repository:**

```bash
git clone https://github.com/Hugosh71/Projet_Mangetamain.git
cd Projet_Mangetamain
```

1. **Build the Docker image:**

```bash
docker build -t mangetamain:latest .
```

1. **Run the container:**

```bash
docker run --rm -it -p 8501:8501 mangetamain:latest
```

## Method 3: Using Docker Compose

For development with all services:

1. **Clone the repository:**

```bash
git clone https://github.com/Hugosh71/Projet_Mangetamain.git
cd Projet_Mangetamain
```

1. **Run with Docker Compose:**

```bash
docker compose up app
```

## Verification

After installation, verify that everything is working correctly:

1. **Check Python version:**

```bash
python --version
```

1. **Check Poetry installation:**

```bash
poetry --version
```

1. **Check dependencies:**

```bash
poetry show
```

1. **Run tests:**

```bash
make test
```

1. **Access the application:**

   Open your browser and navigate to http://localhost:8501

## Troubleshooting

Common Issues

**Issue: Python version mismatch**

```bash
# Solution: Use the correct Python version
poetry env use python3.12
```

**Issue: Virtual environment not activated**

```bash
# Solution: Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
.\.venv\Scripts\activate.ps1  # Windows
```

**Issue: Dependencies not installed**

```bash
# Solution: Reinstall dependencies
poetry install
```

**Issue: Port already in use**

```bash
# Solution: Use a different port
poetry run streamlit run src/app/main.py --server.port=8502
```

## Next Steps

After successful installation, you can:

1. Read the [Usage Guide](../usage/index.md) guide to learn how to use the application
2. Explore the [API Reference](../api/index.md) for detailed API documentation
3. Check the [Development Guide](../development/index.md) guide for contributing to the project
