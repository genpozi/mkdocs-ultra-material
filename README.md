# MkDocs Ultra Material

<div align="center">

![MkDocs Ultra Material](https://img.shields.io/badge/MkDocs-Ultra%20Material-blue?style=for-the-badge)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue?style=flat-square)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![MkDocs](https://img.shields.io/badge/MkDocs-1.5%2B-blue?style=flat-square)](https://www.mkdocs.org/)

**AI-Powered Documentation Generation for MkDocs**

Transform your documentation workflow with intelligent content generation, templates, and automation.

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Examples](#-examples)

</div>

---

## 🚀 What is MkDocs Ultra Material?

MkDocs Ultra Material is an AI-powered plugin for MkDocs that revolutionizes documentation creation. Generate comprehensive documentation from simple prompts, use intelligent templates, and automate your entire documentation workflow.

### Why MkDocs Ultra Material?

- ⚡ **10x Faster**: Generate documentation in minutes, not hours
- 🎯 **Consistent Quality**: Templates ensure uniform documentation across projects
- 🤖 **AI-Powered**: Leverage multiple AI providers (OpenRouter, Gemini, Claude, Ollama)
- 🔄 **Automated**: Integrate with Git, CI/CD, and daily workflows
- 💰 **Cost-Effective**: Smart caching reduces API costs by 80%+
- 📚 **Comprehensive**: 50+ proven prompts, 40+ use cases, complete guides

---

## ✨ Features

### 🎨 Document Generation

Generate documentation from:
- **CLI Commands**: Quick one-liners for instant docs
- **Templates**: Jinja2-based templates for consistent structure
- **Inline Comments**: `<!-- AI-GENERATE: ... -->` syntax in markdown
- **Context Files**: YAML-based context for complex documents

### 🔌 Multiple AI Providers

- **OpenRouter**: Access 100+ models through one API
- **Google Gemini**: Fast, cost-effective generation
- **Anthropic Claude**: High-quality, nuanced content
- **Ollama**: Local, private AI models

### 🎯 Smart Features

- **Intelligent Caching**: Disk-based cache with 24-hour TTL
- **Template System**: Reusable Jinja2 templates
- **MkDocs Integration**: Seamless build-time generation
- **Cost Optimization**: Automatic caching and batching
- **Error Handling**: Graceful fallbacks and retries

### 🛠️ Developer Experience

- **CLI Tool**: Powerful `mkdocs-ai` command
- **Git Hooks**: Pre-commit documentation checks
- **CI/CD Ready**: GitHub Actions, GitLab CI examples
- **IDE Integration**: VS Code, JetBrains support
- **Type Safety**: Full type hints and validation

---

## 📦 Installation

### From PyPI (Coming Soon)

```bash
pip install mkdocs-ultra-material
```

### From Source

```bash
git clone https://github.com/genpozi/mkdocs-ultra-material.git
cd mkdocs-ultra-material
pip install -e .
```

### Requirements

- Python 3.9+
- MkDocs 1.5+
- API key for chosen provider (OpenRouter, Gemini, etc.)

---

## 🚀 Quick Start

### 1. Configure API Key

```bash
export OPENROUTER_API_KEY="your-api-key-here"
# or
export GEMINI_API_KEY="your-api-key-here"
```

### 2. Add to mkdocs.yml

```yaml
plugins:
  - mkdocs-ai:
      provider: openrouter
      model: anthropic/claude-3.5-sonnet
      cache_enabled: true
      cache_ttl: 86400
```

### 3. Generate Documentation

**From CLI**:
```bash
# Simple generation
mkdocs-ai generate \
  --prompt "Create API documentation for my REST service" \
  --output docs/api.md

# Using templates
mkdocs-ai generate \
  --template templates/homelab-service.md.j2 \
  --context examples/homelab-plex.yaml \
  --output docs/services/plex.md
```

**In Markdown**:
```markdown
# My Documentation

## Troubleshooting

<!-- AI-GENERATE: Create a troubleshooting guide for common Docker networking issues -->
```

Then build:
```bash
mkdocs build
```

---

## 📚 Documentation

### Core Guides

- **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- **[Usage Guide](USAGE_GUIDE.md)** - Complete CLI reference
- **[Daily Use Guide](DAILY_USE_GUIDE.md)** - Integrate into your workflow

### Comprehensive Resources

- **[Practical Examples](PRACTICAL_EXAMPLES.md)** - 25+ copy-paste examples
- **[Use Cases Library](USE_CASES.md)** - 40+ documented use cases
- **[Prompt Library](PROMPT_LIBRARY.md)** - 50+ proven prompts
- **[Integration Patterns](INTEGRATION_PATTERNS.md)** - Git, CI/CD, IDE integration

### Planning & Strategy

- **[Site Structure Plan](SITE_STRUCTURE_PLAN.md)** - Complete site architecture
- **[Meta-Documentation Strategy](META_DOCUMENTATION_STRATEGY.md)** - Self-documenting approach
- **[Implementation Status](IMPLEMENTATION_STATUS.md)** - Current progress

---

## 💡 Examples

### Homelab Documentation

```bash
mkdocs-ai generate \
  --prompt "Document my Plex Media Server running on Docker with:
- Container configuration
- Port mappings (32400)
- Volume mounts for media
- Backup procedures
- Common troubleshooting" \
  --output docs/homelab/plex.md
```

### Research Reports

```bash
mkdocs-ai generate \
  --template templates/research-report.md.j2 \
  --context examples/research-ai-agents.yaml \
  --output research/ai-agents-comparison.md
```

### API Documentation

```bash
mkdocs-ai generate \
  --prompt "Document REST API with endpoints:
- GET /users - List users
- POST /users - Create user
- GET /users/{id} - Get user
Include request/response examples and error codes" \
  --output docs/api/users.md
```

---

## 🎯 Use Cases

### Personal Knowledge Management
- Daily knowledge capture
- Meeting notes enhancement
- Learning journals
- Book summaries

### Homelab Documentation
- Service documentation
- Network topology
- Backup strategies
- Maintenance runbooks

### Research & Analysis
- Research reports
- Literature reviews
- Technology evaluations
- Experiment documentation

### Software Development
- API documentation
- Architecture docs
- Migration guides
- Troubleshooting guides

### Team Documentation
- Onboarding guides
- Process documentation
- Decision records (ADRs)
- Team playbooks

[See all 40+ use cases →](USE_CASES.md)

---

## 🗺️ Roadmap

### ✅ Priority 1: Document Generation (Complete)
- [x] CLI tool with full options
- [x] Template system with Jinja2
- [x] Markdown syntax (AI-GENERATE comments)
- [x] Multiple AI providers
- [x] Smart caching system
- [x] MkDocs plugin integration

### 🚧 Priority 2: Content Enhancement (Planned)
- [ ] Enhance existing documentation
- [ ] Improve clarity and structure
- [ ] Add missing sections
- [ ] Update outdated content

### 📋 Priority 3: Semantic Search (Planned)
- [ ] Vector embeddings
- [ ] Semantic search interface
- [ ] Context-aware results
- [ ] Search analytics

### 🎨 Priority 4: Asset Processing (Planned)
- [ ] Image analysis and documentation
- [ ] Diagram generation
- [ ] Video transcription
- [ ] Asset optimization

### 💬 Priority 5: Obelisk Integration (Planned)
- [ ] Chatbot interface
- [ ] Interactive documentation
- [ ] Real-time assistance
- [ ] User feedback loop

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Issues**: Found a bug? [Open an issue](https://github.com/genpozi/mkdocs-ultra-material/issues)
2. **Suggest Features**: Have an idea? [Start a discussion](https://github.com/genpozi/mkdocs-ultra-material/discussions)
3. **Submit PRs**: Code contributions welcome!
4. **Share Examples**: Add your use cases and templates
5. **Improve Docs**: Documentation improvements always appreciated

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

Built with amazing open-source tools:

- **[MkDocs](https://www.mkdocs.org/)** - Fast, simple static site generator
- **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** - Beautiful Material Design theme
- **[OpenRouter](https://openrouter.ai/)** - Unified API for 100+ AI models
- **[Anthropic Claude](https://www.anthropic.com/)** - Advanced AI assistant
- **[Google Gemini](https://deepmind.google/technologies/gemini/)** - Fast, efficient AI
- **[Ollama](https://ollama.ai/)** - Local AI model runner

---

## 📊 Stats

- **140KB** of comprehensive documentation
- **50+** proven prompts
- **40+** documented use cases
- **25+** practical examples
- **10+** integration patterns
- **2** production-ready templates

---

## 🌟 Star History

If you find MkDocs Ultra Material useful, please consider giving it a star! ⭐

---

## 📞 Support

- **Documentation**: [Full documentation](https://github.com/genpozi/mkdocs-ultra-material)
- **Issues**: [GitHub Issues](https://github.com/genpozi/mkdocs-ultra-material/issues)
- **Discussions**: [GitHub Discussions](https://github.com/genpozi/mkdocs-ultra-material/discussions)

---

<div align="center">

**Made with ❤️ by the MkDocs Ultra Material Team**

[⬆ Back to Top](#mkdocs-ultra-material)

</div>
