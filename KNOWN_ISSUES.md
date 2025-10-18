# Known Issues and Limitations

**Version**: 0.5.0 Beta  
**Last Updated**: October 18, 2025

---

## Current Limitations

### 1. Streaming Not Implemented

**Status**: Placeholder only  
**Impact**: Medium  
**Affected**: All providers

All AI providers have TODO comments for streaming support. Currently, all generation is blocking.

**Workaround**: Use smaller prompts or run generation in background.

**Planned**: v0.6.0

---

### 2. No Actual AI API Calls in Tests

**Status**: Tests use mocks  
**Impact**: Low  
**Affected**: Test suite

Unit tests don't make real API calls, so actual provider functionality isn't tested.

**Workaround**: Manual testing with real API keys required.

**Planned**: Add integration tests with real API calls (optional, requires API keys).

---

### 3. Plugin TODOs Not Implemented

**Status**: Partial implementation  
**Impact**: Medium  
**Affected**: Plugin hooks

The plugin has several TODO items:

- `on_pre_build`: Process generation tasks from config
- `on_pre_build`: Process asset sources  
- `on_page_markdown`: Apply content enhancement if enabled
- `on_post_build`: Export to Obelisk format if enabled

**Workaround**: Use CLI commands instead of automatic processing.

**Planned**: v0.6.0

---

### 4. Search Requires Manual Index Build

**Status**: Working but manual  
**Impact**: Low  
**Affected**: Semantic search

Search index must be built manually with `mkdocs-ai search build` command.

**Workaround**: Add to build script or CI/CD pipeline.

**Planned**: Automatic build during `mkdocs build` in v0.6.0.

---

### 5. No Rate Limiting

**Status**: Not implemented  
**Impact**: Medium  
**Affected**: All providers

No built-in rate limiting for API calls. Can hit provider rate limits.

**Workaround**: Use caching aggressively, add delays between calls manually.

**Planned**: v0.6.0

---

### 6. Limited Error Recovery

**Status**: Basic retry logic only  
**Impact**: Medium  
**Affected**: All providers

Providers have basic retry with exponential backoff, but no circuit breaker pattern.

**Workaround**: Monitor logs and retry failed operations manually.

**Planned**: v0.7.0

---

### 7. No Batch Processing

**Status**: Not implemented  
**Impact**: Low  
**Affected**: CLI generation

Cannot generate multiple documents in parallel.

**Workaround**: Use shell scripts with background processes.

**Planned**: v0.7.0

---

### 8. Obelisk Integration Untested

**Status**: Implemented but untested  
**Impact**: High  
**Affected**: Obelisk module

Obelisk integration is complete but hasn't been tested with a real Obelisk instance.

**Workaround**: None - requires Obelisk server for testing.

**Planned**: Test with Obelisk v1.0 when available.

---

### 9. Asset Processing Not Automatic

**Status**: CLI only  
**Impact**: Medium  
**Affected**: Asset processing

Asset processing must be triggered manually via CLI, not automatic during build.

**Workaround**: Add `mkdocs-ai assets process` to build script.

**Planned**: Automatic processing in v0.6.0.

---

### 10. No Multi-language Support

**Status**: English only  
**Impact**: Low  
**Affected**: All features

System prompts and documentation are English-only.

**Workaround**: Provide custom system prompts in target language.

**Planned**: v1.0.0

---

## Known Bugs

### None Currently Identified

All known issues are limitations, not bugs. Report bugs at:
https://github.com/genpozi/mkdocs-ultra-material/issues

---

## Performance Considerations

### 1. Cache Size

**Issue**: Cache can grow large with many generations.

**Mitigation**: 
- Default max size: 100MB
- Automatic LRU eviction
- Manual cleanup: `mkdocs-ai cache clear`

### 2. Embedding Generation

**Issue**: Generating embeddings for large sites is slow.

**Mitigation**:
- Embeddings are cached
- Only regenerate when content changes
- Use smaller chunk sizes for faster processing

### 3. API Costs

**Issue**: AI API calls can be expensive.

**Mitigation**:
- Aggressive caching (24-hour TTL)
- Use free models for testing (llama-4-maverick:free)
- Monitor usage with provider dashboards

---

## Security Considerations

### 1. API Keys in Environment

**Status**: Current best practice  
**Risk**: Low

API keys are stored in environment variables, not in code.

**Recommendation**: Use secrets management in production (e.g., GitHub Secrets, AWS Secrets Manager).

### 2. No Secrets Scanning

**Status**: Not implemented  
**Risk**: Medium

No automated scanning for accidentally committed secrets.

**Mitigation**: 
- Use pre-commit hooks
- Add `.env` to `.gitignore`
- Review commits before pushing

### 3. Untrusted Content

**Status**: No sanitization  
**Risk**: Low

AI-generated content is not sanitized before insertion into documentation.

**Mitigation**: Review generated content before publishing.

---

## Compatibility

### Python Versions

**Supported**: 3.11, 3.12  
**Tested**: 3.11  
**Not Supported**: <3.11

Requires Python 3.11+ for modern type hints and async features.

### MkDocs Versions

**Supported**: 1.6.0+  
**Tested**: 1.6.0  
**Not Supported**: <1.6.0

Requires MkDocs 1.6.0+ for plugin API compatibility.

### Operating Systems

**Tested**: Linux (Ubuntu 24.04)  
**Expected to work**: macOS, Windows  
**Not tested**: Windows, macOS

Development and testing done on Linux. Should work on other platforms but not tested.

---

## Workarounds and Tips

### 1. Slow Generation

**Problem**: Generation takes too long.

**Solutions**:
- Use faster models (e.g., Gemini Flash)
- Reduce `max_tokens` setting
- Enable caching
- Use smaller prompts

### 2. Cache Misses

**Problem**: Cache not being used.

**Solutions**:
- Ensure prompts are identical (whitespace matters)
- Check cache TTL hasn't expired
- Verify cache directory is writable
- Check cache stats: `mkdocs-ai cache stats`

### 3. Provider Errors

**Problem**: API calls failing.

**Solutions**:
- Verify API key is correct
- Check provider status page
- Try fallback model
- Increase timeout setting
- Check rate limits

### 4. Memory Usage

**Problem**: High memory usage during build.

**Solutions**:
- Reduce chunk size for search
- Process assets in smaller batches
- Clear cache periodically
- Use streaming (when implemented)

---

## Reporting Issues

### Before Reporting

1. Check this document for known issues
2. Search existing issues on GitHub
3. Try with latest version
4. Test with minimal configuration

### When Reporting

Include:

- MkDocs Ultra Material version
- Python version
- Operating system
- MkDocs configuration (sanitized)
- Error messages and logs
- Steps to reproduce

### Where to Report

- **Bugs**: https://github.com/genpozi/mkdocs-ultra-material/issues
- **Questions**: https://github.com/genpozi/mkdocs-ultra-material/discussions
- **Security**: Email maintainers (see README)

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features and timeline.

---

**Note**: This is beta software. Expect rough edges and breaking changes before v1.0.0.
