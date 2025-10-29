# syntax=docker/dockerfile:1

### ---------- Base builder stage ----------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Install build dependencies (needed only for building wheels)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the dependency files first (to leverage Docker cache)
COPY pyproject.toml README.md ./

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Install only required groups (exclude heavy 'ml', include 'ui')
RUN poetry config virtualenvs.create false \
    && poetry install --with ui --without ml --no-root \
    && poetry cache clear pypi --all --no-interaction \
    && rm -rf /tmp/poetry_cache

# Copy the actual source code last
COPY src/ ./src/

### ---------- Final runtime stage ----------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

COPY --from=builder /usr/local /usr/local


# Copy all sources
COPY src/ ./src/
COPY .streamlit/ ./src/.streamlit/
COPY data/ ./data/

EXPOSE 8501
CMD ["streamlit", "run", "src/app/main.py"]
