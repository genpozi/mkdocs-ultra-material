FROM mcr.microsoft.com/devcontainers/python:3.11

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    git \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspaces/mkdocs-ultra-material

# Copy dependency files
COPY pyproject.toml README.md ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir hatchling

# Install the package in editable mode with dev dependencies
RUN pip install --no-cache-dir -e ".[dev,search]"

# Install additional useful tools
RUN pip install --no-cache-dir \
    ipython \
    pre-commit
