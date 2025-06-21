# Stage 1: Base image with Python and uv
FROM python:3.11.12-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency manifests
COPY pyproject.toml uv.lock ./

# Create a virtual environment and install dependencies
RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv pip install --no-cache-dir -e .

# Copy the project into the intermediate image
ADD . /app

# Stage 2: Final image
FROM python:3.11.12-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

# Change the working directory to the `app` directory
WORKDIR /app

# Copy the uv-managed virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Copy the application code from the builder
COPY --from=builder /app /app

# Ensure the venv is used
ENV PATH="/app/.venv/bin:${PATH}"


CMD ["fastapi", "run", "src/main.py", "--port", "8000"]