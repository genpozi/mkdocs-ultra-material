# Welcome to MkDocs Ultra Material

<div align="center">

![MkDocs Ultra Material](https://img.shields.io/badge/MkDocs-Ultra%20Material-blue?style=for-the-badge)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

**AI-Powered Documentation Generation for MkDocs**

Transform your documentation workflow with intelligent content generation, templates, and automation.

[Quick Start](QUICK_START.md){ .md-button .md-button--primary }
[View on GitHub](https://github.com/genpozi/mkdocs-ultra-material){ .md-button }

</div>

---

## What is MkDocs Ultra Material?

MkDocs Ultra Material is an AI-powered plugin for MkDocs that revolutionizes documentation creation. Generate comprehensive documentation from simple prompts, use intelligent templates, and automate your entire documentation workflow.

### Why Choose MkDocs Ultra Material?

<div class="grid cards" markdown>

-   :zap: **10x Faster**

    ---

    Generate documentation in minutes, not hours. AI-powered generation accelerates your workflow.

-   :dart: **Consistent Quality**

    ---

    Templates ensure uniform documentation across projects. Maintain high standards effortlessly.

-   :robot: **AI-Powered**

    ---

    Leverage multiple AI providers (OpenRouter, Gemini, Claude, Ollama) for best results.

-   :arrows_counterclockwise: **Automated**

    ---

    Integrate with Git, CI/CD, and daily workflows. Documentation that updates itself.

-   :moneybag: **Cost-Effective**

    ---

    Smart caching reduces API costs by 80%+. Pay only for what you need.

-   :books: **Comprehensive**

    ---

    50+ proven prompts, 40+ use cases, complete guides. Everything you need to succeed.

</div>

---

## Key Features

### Document Generation

Generate documentation from:

- **CLI Commands**: Quick one-liners for instant docs
- **Templates**: Jinja2-based templates for consistent structure
- **Inline Comments**: `<!-- AI-GENERATE: ... -->` syntax in markdown
- **Context Files**: YAML-based context for complex documents

### Multiple AI Providers

- **OpenRouter**: Access 100+ models through one API
- **Google Gemini**: Fast, cost-effective generation
- **Anthropic Claude**: High-quality, nuanced content
- **Ollama**: Local, private AI models

### Smart Features

- **Intelligent Caching**: Disk-based cache with 24-hour TTL
- **Template System**: Reusable Jinja2 templates
- **MkDocs Integration**: Seamless build-time generation
- **Cost Optimization**: Automatic caching and batching
- **Error Handling**: Graceful fallbacks and retries

---

## Quick Example

=== "CLI"

    ```bash
    mkdocs-ai generate \
      --prompt "Create API documentation for my REST service" \
      --output docs/api.md
    ```

=== "Template"

    ```bash
    mkdocs-ai generate \
      --template templates/homelab-service.md.j2 \
      --context examples/homelab-plex.yaml \
      --output docs/services/plex.md
    ```

=== "Inline"

    ```markdown
    # My Documentation

    ## Troubleshooting

    <!-- AI-GENERATE: Create a troubleshooting guide for common Docker networking issues -->
    ```

---

## Project Status

**Version**: 0.4.0  
**Status**: 80% Complete

- ✅ **Priority 1**: Document Generation (Complete)
- ✅ **Priority 2**: Content Enhancement (Complete)
- ✅ **Priority 3**: Semantic Search (Complete)
- ✅ **Priority 4**: Asset Processing (Complete)
- 🚧 **Priority 5**: Obelisk Integration (In Progress)

---

## Get Started

Ready to transform your documentation workflow?

1. [Quick Start Guide](QUICK_START.md) - Get started in 5 minutes
2. [Usage Guide](USAGE_GUIDE.md) - Complete CLI reference
3. [Practical Examples](PRACTICAL_EXAMPLES.md) - 25+ copy-paste examples

---

## Community

- **GitHub**: [genpozi/mkdocs-ultra-material](https://github.com/genpozi/mkdocs-ultra-material)
- **Issues**: [Report bugs or request features](https://github.com/genpozi/mkdocs-ultra-material/issues)
- **Discussions**: [Join the conversation](https://github.com/genpozi/mkdocs-ultra-material/discussions)

---

<div align="center">

**Made with ❤️ by the MkDocs Ultra Material Team**

[⬆ Back to Top](#welcome-to-mkdocs-ultra-material)

</div>
