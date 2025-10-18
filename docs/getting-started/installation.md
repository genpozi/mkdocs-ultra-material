# Installation

## Requirements

- Python 3.11 or higher
- MkDocs 1.6.0 or higher
- API key for chosen provider (OpenRouter, Gemini, Claude, or Ollama)

## Installation Methods

### From PyPI (Coming Soon)

```bash
pip install mkdocs-ultra-material
```

### From Source

```bash
# Clone the repository
git clone https://github.com/genpozi/mkdocs-ultra-material.git
cd mkdocs-ultra-material

# Install in editable mode
pip install -e .

# Install with optional dependencies
pip install -e ".[dev,search]"
```

### Using Docker

```bash
# Pull the Docker image
docker pull ghcr.io/genpozi/mkdocs-ultra-material:latest

# Or build locally
docker build -t mkdocs-ultra-material .
```

## Verify Installation

```bash
# Check CLI is available
mkdocs-ai --version

# Check plugin is registered
mkdocs plugins
```

You should see `mkdocs-ai` in the list of available plugins.

## Next Steps

- [Quick Start Guide](../QUICK_START.md) - Get started in 5 minutes
- [API Keys Setup](../API_KEYS_SETUP.md) - Configure your AI provider
- [Usage Guide](../USAGE_GUIDE.md) - Learn all the features
