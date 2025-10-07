# syntax=docker/dockerfile:1

### ---------- Base builder stage ----------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install build dependencies (needed only for building wheels)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the dependency files first (to leverage Docker cache)
COPY pyproject.toml README.md ./

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Install only **production** dependencies, no dev, no project itself
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root

# Copy the actual source code last
COPY src/ ./src/
COPY docs/ ./docs/

### ---------- Final runtime stage ----------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy installed packages from builder (this avoids reinstalling everything)
COPY --from=builder /usr/local /usr/local

# Copy only the source code
COPY src/ ./src/
COPY docs/ ./docs/
COPY .streamlit/ ./.streamlit/

EXPOSE 8501

CMD ["streamlit", "run", "src/app/main.py"]
