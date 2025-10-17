# MkDocs AI Assistant - Quick Reference

**Version**: 0.3.0  
**Status**: 3 of 5 priorities complete (60%)

---

## 🚀 Quick Start

### 1. Install

```bash
cd /workspaces/mkdocs-ultra-material
pip install -e .
```

### 2. Set API Key

```bash
export OPENROUTER_API_KEY=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
```

### 3. Generate Documentation

```bash
mkdocs-ai generate "Write a Docker guide" \
  --provider openrouter \
  --model meta-llama/llama-4-maverick:free
```

---

## 📋 Available Commands

### Document Generation

```bash
# Basic generation
mkdocs-ai generate "Your prompt here"

# With output file
mkdocs-ai generate "API documentation" -o docs/api.md

# With template
mkdocs-ai generate "Service docs" \
  -t templates/service.md.j2 \
  -c name=auth -c version=2.0

# With specific model
mkdocs-ai generate "Guide" \
  --model meta-llama/llama-4-maverick:free
```

### Content Enhancement

```bash
# Preview changes
mkdocs-ai enhance docs/index.md --preview

# Apply changes
mkdocs-ai enhance docs/index.md --apply

# Interactive mode
mkdocs-ai enhance docs/index.md --interactive

# Specific features
mkdocs-ai enhance docs/index.md \
  --grammar --clarity --consistency
```

### Semantic Search

```bash
# Build search index
mkdocs-ai search build

# Search documentation
mkdocs-ai search query "docker networking"

# Show statistics
mkdocs-ai search stats

# With options
mkdocs-ai search query "troubleshooting" \
  --limit 5 \
  --semantic-weight 0.8
```

### Cache Management

```bash
# Show cache stats
mkdocs-ai cache-stats

# Clear cache
mkdocs-ai cache-clear
```

---

## 🔑 API Keys

### OpenRouter (Recommended)
```bash
export OPENROUTER_API_KEY=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
```

### Google Gemini
```bash
export GEMINI_API_KEY=AIzaSyBMGIp07y55y96lqIPe6SehC5TJH82ZZ54
```

---

## 🤖 Free Models

### Recommended (OpenRouter)

1. **meta-llama/llama-4-maverick:free** - Best overall
2. **deepseek/deepseek-chat-v3-0324:free** - Technical content
3. **z-ai/glm-4.5-air:free** - Fast responses
4. **openai/gpt-oss-20b:free** - Very fast

---

## ⚙️ Configuration

### Basic mkdocs.yml

```yaml
plugins:
  - ai-assistant:
      provider:
        name: openrouter
        api_key: !ENV OPENROUTER_API_KEY
        model: meta-llama/llama-4-maverick:free
        fallback: deepseek/deepseek-chat-v3-0324:free
      
      cache:
        enabled: true
        dir: .ai-cache
      
      generation:
        enabled: true
      
      enhancement:
        enabled: true
      
      search:
        enabled: true
```

---

## 📊 Features Status

### ✅ Priority 1: Document Generation
- CLI generation
- Template-based generation
- Markdown syntax (AI-GENERATE comments)
- Context variables
- Multiple providers

### ✅ Priority 2: Content Enhancement
- Grammar and spelling
- Clarity improvements
- Consistency checking
- Preview/apply modes
- Interactive review

### ✅ Priority 3: Semantic Search
- Vector embeddings
- Hybrid search (semantic + keyword)
- CLI search commands
- Index management
- Statistics

### 🎯 Priority 4: Asset Processing (Next)
- Docker Compose → Docs
- Code → API docs
- Auto-discovery

### 🎯 Priority 5: Obelisk Integration (Future)
- RAG chatbot
- Interactive docs
- Real-time assistance

---

## 🔧 Common Tasks

### Generate from Template

```bash
mkdocs-ai generate "Service documentation" \
  --template templates/homelab-service.md.j2 \
  --context examples/homelab-plex.yaml \
  --output docs/services/plex.md
```

### Enhance Multiple Files

```bash
for file in docs/*.md; do
  mkdocs-ai enhance "$file" --apply --grammar --clarity
done
```

### Build and Search

```bash
# Build docs with search index
mkdocs build

# Search the index
mkdocs-ai search query "your search term"
```

### Use Different Providers

```bash
# OpenRouter
mkdocs-ai generate "Guide" --provider openrouter

# Gemini
mkdocs-ai generate "Guide" --provider gemini

# With specific model
mkdocs-ai generate "Guide" \
  --provider openrouter \
  --model deepseek/deepseek-chat-v3-0324:free
```

---

## 📁 Project Structure

```
mkdocs-ultra-material/
├── mkdocs_ai/              # Main package
│   ├── providers/          # AI providers
│   ├── generation/         # Document generation
│   ├── enhancement/        # Content enhancement
│   ├── search/            # Semantic search
│   ├── cache/             # Caching system
│   ├── cli.py             # CLI commands
│   ├── plugin.py          # MkDocs plugin
│   └── config.py          # Configuration
├── templates/             # Jinja2 templates
├── examples/              # Example files
├── tests/test_site/       # Test site
└── docs/                  # Documentation
```

---

## 🐛 Troubleshooting

### API Key Not Found

```bash
# Check if set
echo $OPENROUTER_API_KEY

# Set it
export OPENROUTER_API_KEY=sk-or-v1-...
```

### Cache Issues

```bash
# Clear cache
mkdocs-ai cache-clear

# Check stats
mkdocs-ai cache-stats
```

### Slow Generation

```bash
# Use faster model
--model openai/gpt-oss-20b:free

# Enable caching (default)
cache:
  enabled: true
```

### Search Not Working

```bash
# Rebuild index
mkdocs-ai search build --verbose

# Check if enabled
# In mkdocs.yml:
search:
  enabled: true
```

---

## 📚 Documentation

- **[README.md](README.md)** - Overview and features
- **[QUICK_START.md](QUICK_START.md)** - Getting started guide
- **[API_KEYS_SETUP.md](API_KEYS_SETUP.md)** - API keys configuration
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Complete CLI reference
- **[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)** - Current progress

### Examples
- **[examples/search-example.md](examples/search-example.md)** - Search usage
- **[PRACTICAL_EXAMPLES.md](PRACTICAL_EXAMPLES.md)** - 25+ examples
- **[USE_CASES.md](USE_CASES.md)** - 40+ use cases
- **[PROMPT_LIBRARY.md](PROMPT_LIBRARY.md)** - 50+ prompts

---

## 🔗 Links

- **GitHub**: [https://github.com/genpozi/mkdocs-ultra-material](https://github.com/genpozi/mkdocs-ultra-material)
- **Preview**: [https://8000--0199f228-e559-7bce-af81-db717fed5a2b.us-east-1-01.gitpod.dev](https://8000--0199f228-e559-7bce-af81-db717fed5a2b.us-east-1-01.gitpod.dev)

---

## 💡 Tips

1. **Use caching** - Saves API calls and speeds up builds
2. **Start with free models** - Test before using paid models
3. **Enable search** - Improves documentation discoverability
4. **Use templates** - Consistent documentation structure
5. **Preview before applying** - Review enhancements first

---

## 🎯 Next Steps

1. ✅ Set up API keys
2. ✅ Test document generation
3. ✅ Build search index
4. Try content enhancement
5. Explore templates
6. Integrate into workflow

---

**Last Updated**: October 17, 2025
