# Multi-stage build for reddit-agent
ARG ARCH=
FROM --platform=${ARCH} python:3.13-slim-bookworm AS builder

# Install build dependencies for Rust-based packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files and source code
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

# Install dependencies
RUN uv sync --frozen --no-dev

FROM --platform=${ARCH} python:3.13-slim-bookworm AS runtime

# Re-declare ARG for runtime stage
ARG ARCH=

# Install runtime dependencies for Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Make sure we use venv
ENV PATH="/app/.venv/bin:$PATH"

# Install Playwright browsers (Chromium) and system dependencies
RUN playwright install --with-deps chromium

# Copy source code and resources
COPY src/ ./src/

# Run the main.py script
CMD ["python", "-m", "ai_product_research.main"]