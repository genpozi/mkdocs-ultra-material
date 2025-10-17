# Dockerfile for MkDocs AI Assistant
# Extends official MkDocs Material image with AI capabilities

FROM squidfunk/mkdocs-material:latest

# Install system dependencies
RUN apk add --no-cache \
    git \
    build-base \
    python3-dev

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml README.md LICENSE ./
COPY mkdocs_ai/ ./mkdocs_ai/
COPY templates/ ./templates/
COPY examples/ ./examples/

# Install the package and dependencies
RUN pip install --no-cache-dir -e .

# Install additional plugins for enhanced functionality
RUN pip install --no-cache-dir \
    mkdocstrings[python]>=0.24.0 \
    mkdocs-mermaid2-plugin>=1.1.0 \
    mkdocs-awesome-pages-plugin>=2.9.0 \
    mkdocs-minify-plugin>=0.8.0 \
    mkdocs-redirects>=1.2.0

# Expose MkDocs default port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MKDOCS_SERVE_HOST=0.0.0.0

# Default command: serve documentation
CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000"]
