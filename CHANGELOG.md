# Changelog

All notable changes to MkDocs Ultra Material will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0-beta] - 2025-10-18

### Added

#### Core Features
- Complete document generation system with CLI and plugin
- AI-powered content enhancement (grammar, clarity, consistency)
- Semantic search with vector embeddings
- Asset processing for Python code and Docker Compose
- Obelisk integration for RAG chatbots

#### Providers
- OpenRouter provider with 100+ model access
- Google Gemini provider
- Anthropic Claude provider
- Ollama provider for local models
- Provider abstraction layer with fallback support

#### Generation
- CLI generation command with multiple options
- Template-based generation with Jinja2
- Markdown syntax (`<!-- AI-GENERATE: ... -->`)
- Context variables support
- Smart caching system (24-hour TTL)

#### Enhancement
- Grammar and spelling corrections
- Clarity improvements
- Consistency checking
- Content preservation (code, frontmatter, HTML)
- Preview/apply/interactive modes
- Diff generation

#### Search
- Vector embeddings generation
- Hybrid search (semantic + keyword)
- Smart text chunking with overlap
- BM25 keyword scoring
- Cosine similarity for semantic search
- JSON-based index (portable)
- CLI search commands

#### Assets
- Python code documentation with mkdocstrings
- Docker Compose documentation
- Mermaid diagram generation (6 types)
- Auto-discovery system
- AI-enhanced summaries and examples

#### Obelisk
- Async HTTP client for Obelisk API
- Documentation exporter (HTML → Obelisk format)
- Analytics for documentation gap detection
- CLI commands (export, upload, gaps)
- Batch upload support

#### Infrastructure
- GitHub Actions CI/CD pipeline
- Docker support (Dockerfile + Compose)
- Pre-commit hooks configuration
- Dev container with Python 3.11
- Automated testing (52 tests)
- Automated releases
- Documentation deployment

#### Documentation
- Comprehensive README (updated)
- Quick Start Guide
- Usage Guide
- API Keys Setup Guide
- Daily Use Guide
- Practical Examples (25+)
- Use Cases Library (40+)
- Prompt Library (50+)
- Integration Patterns
- Docker Guide
- Contributing Guide
- Beta Testing Guide
- Known Issues documentation
- Beta Release Status
- Final Review Summary
- Self-hosted documentation site

### Changed
- Package name standardized to `mkdocs-ultra-material`
- Plugin name changed from `ai-assistant` to `mkdocs-ai`
- Version bumped to 0.5.0
- Dev container completely rebuilt with Python 3.11

### Fixed
- Dev container now includes Python environment
- Package naming inconsistencies resolved
- Search module imports corrected (SearchChunk → PageChunk)
- Cache test methods updated (stats() → get_stats())
- Test fixtures corrected (sample_response)
- Missing beautifulsoup4 dependency added

### Dependencies
- mkdocs>=1.6.0
- httpx>=0.27.0
- pydantic>=2.0.0
- pyyaml>=6.0
- jinja2>=3.1.0
- click>=8.1.0
- rich>=13.0.0
- diskcache>=5.6.0
- beautifulsoup4>=4.12.0 (optional, for obelisk)

### Known Limitations
- Streaming support not implemented (placeholder only)
- Plugin TODOs not implemented (automatic processing)
- No rate limiting
- No batch processing
- Obelisk integration untested with real server
- No multi-language support

See [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for complete list.

## [0.4.0] - 2025-10-17

### Added
- Priority 4: Asset Processing complete
- mkdocstrings integration
- Docker support
- Mermaid diagram generation

## [0.3.0] - 2025-10-17

### Added
- Priority 3: Semantic Search complete
- Vector embeddings
- Hybrid search
- CLI search commands

## [0.2.0] - 2025-10-17

### Added
- Priority 2: Content Enhancement complete
- Grammar and spelling corrections
- Clarity improvements
- Consistency checking

## [0.1.0] - 2025-10-17

### Added
- Priority 1: Document Generation complete
- CLI generation commands
- Template system
- Markdown syntax
- Multiple AI providers
- Caching system

## [0.0.1] - 2025-10-17

### Added
- Initial project structure
- Provider abstraction layer
- Configuration system
- MkDocs plugin scaffolding

---

## Release Notes

### v0.5.0 Beta

This is the first beta release of MkDocs Ultra Material. All 5 core priorities are implemented and ready for testing.

**Highlights**:
- 🎯 Complete feature set (all 5 priorities)
- 🧪 52 tests (unit + integration)
- 📚 250KB+ documentation
- 🚀 Production-ready infrastructure
- 🐳 Docker support
- ⚙️ CI/CD pipeline

**What's Next**:
- v0.6.0: Implement plugin TODOs, streaming, rate limiting
- v0.7.0: Batch processing, performance optimization
- v1.0.0: Production release with security audit

**Feedback Welcome**:
Please test and report issues at: https://github.com/genpozi/mkdocs-ultra-material/issues

---

[Unreleased]: https://github.com/genpozi/mkdocs-ultra-material/compare/v0.5.0-beta...HEAD
[0.5.0-beta]: https://github.com/genpozi/mkdocs-ultra-material/releases/tag/v0.5.0-beta
[0.4.0]: https://github.com/genpozi/mkdocs-ultra-material/releases/tag/v0.4.0
[0.3.0]: https://github.com/genpozi/mkdocs-ultra-material/releases/tag/v0.3.0
[0.2.0]: https://github.com/genpozi/mkdocs-ultra-material/releases/tag/v0.2.0
[0.1.0]: https://github.com/genpozi/mkdocs-ultra-material/releases/tag/v0.1.0
[0.0.1]: https://github.com/genpozi/mkdocs-ultra-material/releases/tag/v0.0.1
