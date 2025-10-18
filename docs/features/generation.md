# Document Generation

The core feature of MkDocs Ultra Material is AI-powered document generation. Generate comprehensive documentation from simple prompts, templates, or inline comments.

## Generation Methods

### 1. CLI Generation

Generate documents directly from the command line:

```bash
mkdocs-ai generate \
  --prompt "Create API documentation for my REST service" \
  --output docs/api.md
```

**Options:**

- `--prompt`: The generation prompt
- `--output`: Output file path
- `--provider`: AI provider (openrouter, gemini, anthropic, ollama)
- `--model`: Specific model to use
- `--template`: Use a Jinja2 template
- `--context`: Template context variables

### 2. Template-Based Generation

Use Jinja2 templates for consistent documentation:

```bash
mkdocs-ai generate \
  --template templates/homelab-service.md.j2 \
  --context examples/homelab-plex.yaml \
  --output docs/services/plex.md
```

**Template Example:**

```jinja2
# {{ service_name }}

{{ ai.summary }}

## Configuration

- **Port**: {{ port }}
- **Volumes**: {{ volumes }}

{{ ai.troubleshooting }}
```

### 3. Inline Markdown Syntax

Generate content directly in your markdown files:

```markdown
# My Documentation

## Overview

<!-- AI-GENERATE: Create an overview of Docker networking concepts -->

## Advanced Topics

<!-- AI-GENERATE-START: networking-deep-dive -->
Explain Docker bridge networks, overlay networks, and host networking
<!-- AI-GENERATE-END -->
```

The plugin processes these comments during `mkdocs build`.

## AI Providers

### OpenRouter (Recommended)

Access 100+ models through one API:

```yaml
plugins:
  - mkdocs-ai:
      provider:
        name: openrouter
        api_key: !ENV OPENROUTER_API_KEY
        model: anthropic/claude-3.5-sonnet
        fallback: meta-llama/llama-4-maverick:free
```

### Google Gemini

Fast and cost-effective:

```yaml
plugins:
  - mkdocs-ai:
      provider:
        name: gemini
        api_key: !ENV GEMINI_API_KEY
        model: gemini-pro
```

### Anthropic Claude

High-quality content:

```yaml
plugins:
  - mkdocs-ai:
      provider:
        name: anthropic
        api_key: !ENV ANTHROPIC_API_KEY
        model: claude-3-5-sonnet-20241022
```

### Ollama

Local, private AI:

```yaml
plugins:
  - mkdocs-ai:
      provider:
        name: ollama
        base_url: http://localhost:11434
        model: llama2
```

## Caching

Smart caching reduces API costs by 80%+:

```yaml
plugins:
  - mkdocs-ai:
      cache:
        enabled: true
        dir: .ai-cache
        ttl: 86400  # 24 hours
        max_size: 1073741824  # 1GB
```

**Cache Management:**

```bash
# View cache statistics
mkdocs-ai cache stats

# Clear cache
mkdocs-ai cache clear

# Clear expired entries
mkdocs-ai cache prune
```

## Best Practices

### 1. Write Clear Prompts

❌ Bad:
```
Write about Docker
```

✅ Good:
```
Create a comprehensive guide to Docker networking including:
- Bridge networks
- Overlay networks
- Host networking
- Common troubleshooting scenarios
Include practical examples for each type.
```

### 2. Use Templates for Consistency

Create reusable templates for common documentation patterns:

- API endpoints
- Service documentation
- Troubleshooting guides
- Configuration references

### 3. Leverage Context Variables

Pass structured data to templates:

```yaml
# context.yaml
service_name: Plex Media Server
port: 32400
volumes:
  - /data/media:/media
  - /data/config:/config
features:
  - Media streaming
  - Remote access
  - Mobile apps
```

### 4. Enable Caching

Always enable caching in production to reduce costs and improve performance.

## Examples

See [Practical Examples](../PRACTICAL_EXAMPLES.md) for 25+ copy-paste examples.

## Next Steps

- [Content Enhancement](enhancement.md) - Improve existing documentation
- [Semantic Search](search.md) - Add AI-powered search
- [Asset Processing](assets.md) - Generate docs from code
