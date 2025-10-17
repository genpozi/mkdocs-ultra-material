# Docker Setup Guide

Complete guide for using MkDocs AI Assistant with Docker.

---

## Quick Start

### 1. Using Docker Compose (Recommended)

```bash
# Start development server
docker-compose up

# Access at http://localhost:8000
```

### 2. Using Docker directly

```bash
# Build image
docker build -t mkdocs-ai .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/docs:/app/docs \
  -v $(pwd)/mkdocs.yml:/app/mkdocs.yml \
  -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY \
  mkdocs-ai
```

---

## Docker Compose Services

### Development Server

Hot-reload enabled for documentation changes:

```bash
# Start server
docker-compose up mkdocs

# Or in detached mode
docker-compose up -d mkdocs

# View logs
docker-compose logs -f mkdocs

# Stop server
docker-compose down
```

**Features**:
- Hot-reload on file changes
- Persistent AI cache
- Source code mounted for development
- Port 8000 exposed

### Build Service

Build static site:

```bash
# Build documentation
docker-compose --profile build up build

# Output in ./site directory
```

### Test Site

Run test site on port 8001:

```bash
# Start test site
docker-compose --profile test up test-site

# Access at http://localhost:8001
```

---

## Environment Variables

Create `.env` file in project root:

```bash
# .env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
GEMINI_API_KEY=your-gemini-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
```

Docker Compose automatically loads this file.

---

## Volume Mounts

### Development Setup

```yaml
volumes:
  - ./docs:/app/docs              # Documentation source
  - ./mkdocs.yml:/app/mkdocs.yml  # Configuration
  - ./.ai-cache:/app/.ai-cache    # AI cache (persistent)
  - ./mkdocs_ai:/app/mkdocs_ai    # Source code (dev only)
```

### Production Setup

```yaml
volumes:
  - ./docs:/app/docs              # Documentation source
  - ./mkdocs.yml:/app/mkdocs.yml  # Configuration
  - ./.ai-cache:/app/.ai-cache    # AI cache (persistent)
  # No source code mount
```

---

## Common Tasks

### Build Documentation

```bash
# Using Docker Compose
docker-compose --profile build up build

# Using Docker directly
docker run --rm \
  -v $(pwd)/docs:/app/docs \
  -v $(pwd)/mkdocs.yml:/app/mkdocs.yml \
  -v $(pwd)/site:/app/site \
  mkdocs-ai mkdocs build
```

### Run CLI Commands

```bash
# Generate documentation
docker-compose run --rm mkdocs \
  mkdocs-ai generate "Docker guide"

# Build search index
docker-compose run --rm mkdocs \
  mkdocs-ai search build

# Enhance content
docker-compose run --rm mkdocs \
  mkdocs-ai enhance docs/index.md --preview
```

### Access Container Shell

```bash
# Using Docker Compose
docker-compose exec mkdocs sh

# Using Docker directly
docker run -it --rm mkdocs-ai sh
```

### Update Dependencies

```bash
# Rebuild image
docker-compose build --no-cache

# Or with Docker
docker build --no-cache -t mkdocs-ai .
```

---

## Customization

### Extend the Image

Create custom Dockerfile:

```dockerfile
# Dockerfile.custom
FROM mkdocs-ai:latest

# Install additional plugins
RUN pip install mkdocs-git-revision-date-localized-plugin

# Add custom theme
COPY custom-theme/ /app/custom-theme/
```

Build:

```bash
docker build -f Dockerfile.custom -t mkdocs-ai-custom .
```

### Add Plugins

Edit `docker-compose.yml`:

```yaml
services:
  mkdocs:
    build:
      context: .
      dockerfile: Dockerfile
    # ... other config ...
    command: >
      sh -c "pip install mkdocs-plugin-name && mkdocs serve -a 0.0.0.0:8000"
```

Or create `requirements-docker.txt`:

```txt
mkdocs-plugin-name>=1.0.0
another-plugin>=2.0.0
```

Update Dockerfile:

```dockerfile
COPY requirements-docker.txt .
RUN pip install -r requirements-docker.txt
```

---

## Troubleshooting

### Port Already in Use

```bash
# Change port in docker-compose.yml
ports:
  - "8080:8000"  # Use 8080 instead

# Or specify when running
docker run -p 8080:8000 mkdocs-ai
```

### Permission Issues

```bash
# Run as current user
docker run --user $(id -u):$(id -g) mkdocs-ai

# Or in docker-compose.yml
services:
  mkdocs:
    user: "${UID}:${GID}"
```

### Cache Not Persisting

Ensure volume is mounted:

```yaml
volumes:
  - ./.ai-cache:/app/.ai-cache
```

Create directory if it doesn't exist:

```bash
mkdir -p .ai-cache
```

### Hot-Reload Not Working

1. Check volume mounts are correct
2. Ensure files are being saved
3. Check Docker logs:

```bash
docker-compose logs -f mkdocs
```

### API Keys Not Working

1. Check `.env` file exists
2. Verify environment variables:

```bash
docker-compose exec mkdocs env | grep API_KEY
```

3. Restart containers:

```bash
docker-compose down
docker-compose up
```

---

## Production Deployment

### Build Optimized Image

```dockerfile
# Dockerfile.prod
FROM squidfunk/mkdocs-material:latest

# Install only production dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy only necessary files
COPY mkdocs_ai/ ./mkdocs_ai/
COPY docs/ ./docs/
COPY mkdocs.yml ./

# Build documentation
RUN mkdocs build

# Serve with lightweight server
FROM nginx:alpine
COPY --from=0 /app/site /usr/share/nginx/html
EXPOSE 80
```

Build and run:

```bash
docker build -f Dockerfile.prod -t mkdocs-ai-prod .
docker run -p 80:80 mkdocs-ai-prod
```

### Docker Hub

```bash
# Tag image
docker tag mkdocs-ai username/mkdocs-ai:latest

# Push to Docker Hub
docker push username/mkdocs-ai:latest

# Pull and run
docker pull username/mkdocs-ai:latest
docker run -p 8000:8000 username/mkdocs-ai:latest
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/docs.yml
name: Build Documentation

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build with Docker
        run: |
          docker-compose --profile build up build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

### GitLab CI

```yaml
# .gitlab-ci.yml
build-docs:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker-compose --profile build up build
  artifacts:
    paths:
      - site/
```

---

## Best Practices

### 1. Use .env for Secrets

Never commit API keys:

```bash
# .env (gitignored)
OPENROUTER_API_KEY=secret-key

# .env.example (committed)
OPENROUTER_API_KEY=your-key-here
```

### 2. Mount Volumes for Development

```yaml
volumes:
  - ./docs:/app/docs  # Hot-reload
  - ./.ai-cache:/app/.ai-cache  # Persistent cache
```

### 3. Use Profiles for Different Environments

```yaml
services:
  dev:
    # ... dev config ...
  
  prod:
    # ... prod config ...
    profiles:
      - production
```

### 4. Keep Images Small

- Use `.dockerignore`
- Multi-stage builds for production
- Clean up in same RUN command

### 5. Health Checks

```yaml
services:
  mkdocs:
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:8000"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## Performance Tips

### 1. Use BuildKit

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Build with BuildKit
docker build --progress=plain -t mkdocs-ai .
```

### 2. Cache Dependencies

```dockerfile
# Copy only requirements first
COPY pyproject.toml ./
RUN pip install -e .

# Then copy source code
COPY mkdocs_ai/ ./mkdocs_ai/
```

### 3. Use Bind Mounts for Development

Faster than volumes on some systems:

```yaml
volumes:
  - type: bind
    source: ./docs
    target: /app/docs
```

---

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [MkDocs Material Docker Image](https://hub.docker.com/r/squidfunk/mkdocs-material/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

**Last Updated**: October 17, 2025
