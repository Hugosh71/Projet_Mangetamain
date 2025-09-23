# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# System deps
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only dependency files first for better caching
COPY pyproject.toml poetry.lock* README.md ./

# Install uv for fast installs (fallback to pip if needed)
RUN pip install --no-cache-dir uv || true

# Install runtime dependencies using pip via uv or pip
RUN if command -v uv >/dev/null 2>&1; then \
      uv pip install --system --requirement <(uv pip compile pyproject.toml --no-emit-index-url --generate-hashes | sed 's/ --hash=.*$//'); \
    else \
      pip install streamlit; \
    fi

# Copy source
COPY src/ ./src/
COPY docs/ ./docs/

EXPOSE 8501

ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

CMD ["streamlit", "run", "src/app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]


