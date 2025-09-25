# Use an official UV Python base image
FROM ghcr.io/astral-sh/uv:python3.10-trixie AS base

# Set working directory inside the container
WORKDIR /app

# Copy configuration files
COPY pyproject.toml uv.lock .python-version ./

# Set environment variables
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=/app/uv.lock \
    --mount=type=bind,source=pyproject.toml,target=/app/pyproject.toml \
    uv sync --frozen --no-dev

# Copy source code
COPY src /app/src

# Copy fastapi source code
COPY server.py /app

# Use an official Python final image
FROM python:3.10-slim-bookworm AS final

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set environment variables
ARG VERSION=0.1.0
ENV APP_VERSION=$VERSION

# Set working directory inside the container
WORKDIR /app

# Copy the virtual environment from the base stage
COPY --from=base /app /app
COPY --from=base /root/.local /root/.local

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose the FastAPI port
EXPOSE 1243

# Run the application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "1243", "--workers", "2"]
