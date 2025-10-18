# Beta Testing Guide

**Version**: 0.5.0 Beta  
**Status**: Ready for Testing  
**Last Updated**: October 18, 2025

---

## Welcome Beta Testers! 🎉

Thank you for helping test MkDocs Ultra Material! This guide will help you get started and provide valuable feedback.

---

## Quick Start

### 1. Prerequisites

- Python 3.11 or 3.12
- Git
- API key for at least one provider (OpenRouter recommended)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/genpozi/mkdocs-ultra-material.git
cd mkdocs-ultra-material

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with all features
pip install -e ".[dev,search,obelisk]"
```

### 3. Get API Keys

**OpenRouter** (Recommended - access to 100+ models):
1. Visit https://openrouter.ai/
2. Sign up for free account
3. Get API key from dashboard
4. Set environment variable:
   ```bash
   export OPENROUTER_API_KEY="your-key-here"
   ```

**Alternative Providers**:
- **Gemini**: https://makersuite.google.com/app/apikey
- **Anthropic**: https://console.anthropic.com/
- **Ollama**: Install locally from https://ollama.ai/

### 4. Verify Installation

```bash
# Check CLI is available
mkdocs-ai --version

# Should output: mkdocs-ai, version 0.5.0

# Check plugin is registered
mkdocs plugins | grep mkdocs-ai
```

---

## Testing Scenarios

### Scenario 1: Basic Document Generation

**Goal**: Test CLI generation with simple prompt.

**Steps**:

1. Create test directory:
   ```bash
   mkdir test-docs
   cd test-docs
   ```

2. Generate a document:
   ```bash
   mkdocs-ai generate \
     "Create a guide about Docker networking basics" \
     --output docker-guide.md
   ```

3. Check the output:
   ```bash
   cat docker-guide.md
   ```

**Expected Result**: 
- File created successfully
- Contains markdown content about Docker networking
- Has proper structure (headings, paragraphs, examples)

**Report**:
- ✅ Success / ❌ Failure
- Quality of generated content (1-5 stars)
- Any errors or issues

---

### Scenario 2: Template-Based Generation

**Goal**: Test template system with context variables.

**Steps**:

1. Create a template file `service-template.md.j2`:
   ```jinja2
   # {{ service_name }}

   {{ ai.overview }}

   ## Configuration

   - **Port**: {{ port }}
   - **Type**: {{ service_type }}

   {{ ai.setup_guide }}

   ## Troubleshooting

   {{ ai.common_issues }}
   ```

2. Create context file `plex-context.yaml`:
   ```yaml
   service_name: Plex Media Server
   port: 32400
   service_type: Media Streaming
   ```

3. Generate document:
   ```bash
   mkdocs-ai generate \
     --template service-template.md.j2 \
     --context plex-context.yaml \
     --output plex-docs.md
   ```

**Expected Result**:
- Template rendered with context variables
- AI fields filled with relevant content
- Proper markdown formatting

**Report**:
- Template rendering works correctly
- AI content is relevant to context
- Any issues with Jinja2 syntax

---

### Scenario 3: MkDocs Integration

**Goal**: Test plugin integration with MkDocs.

**Steps**:

1. Create `mkdocs.yml`:
   ```yaml
   site_name: Test Site
   
   plugins:
     - search
     - mkdocs-ai:
         provider:
           name: openrouter
           api_key: !ENV OPENROUTER_API_KEY
           model: meta-llama/llama-4-maverick:free
         cache:
           enabled: true
   ```

2. Create `docs/index.md`:
   ```markdown
   # Welcome

   ## Docker Guide

   <!-- AI-GENERATE: Explain Docker containers in simple terms -->

   ## Kubernetes

   <!-- AI-GENERATE: Compare Docker and Kubernetes -->
   ```

3. Build the site:
   ```bash
   mkdocs build
   ```

4. Check output:
   ```bash
   cat site/index.html
   ```

**Expected Result**:
- Build completes successfully
- AI-GENERATE comments replaced with content
- HTML output contains generated text

**Report**:
- Plugin loads correctly
- AI comments processed
- Build time (seconds)
- Any errors in logs

---

### Scenario 4: Caching

**Goal**: Verify caching reduces API calls.

**Steps**:

1. Generate document first time:
   ```bash
   time mkdocs-ai generate \
     "Explain Python decorators" \
     --output decorators1.md
   ```
   Note the time taken.

2. Generate same document again:
   ```bash
   time mkdocs-ai generate \
     "Explain Python decorators" \
     --output decorators2.md
   ```
   Note the time taken.

3. Check cache stats:
   ```bash
   mkdocs-ai cache stats
   ```

**Expected Result**:
- Second generation much faster (cached)
- Cache stats show hits
- Both files have identical content

**Report**:
- First generation time: ___ seconds
- Second generation time: ___ seconds
- Cache hit rate: ___%
- Any cache issues

---

### Scenario 5: Search Index

**Goal**: Test semantic search functionality.

**Steps**:

1. Build a test site (use Scenario 3 setup)

2. Build search index:
   ```bash
   mkdocs-ai search build --site-dir site
   ```

3. Query the index:
   ```bash
   mkdocs-ai search query "how do containers work"
   ```

4. Check statistics:
   ```bash
   mkdocs-ai search stats
   ```

**Expected Result**:
- Index builds successfully
- Queries return relevant results
- Stats show chunk count and pages

**Report**:
- Index build time: ___ seconds
- Query response time: ___ ms
- Result relevance (1-5 stars)
- Any errors

---

### Scenario 6: Content Enhancement

**Goal**: Test AI-powered content improvement.

**Steps**:

1. Create a document with errors `test-doc.md`:
   ```markdown
   # Docker Guid

   Docker is a platfrom for containerization. It allow you to
   package applications with there dependencies.

   ## Benifits

   - Easy deployment
   - Consistant environments
   - Scalability
   ```

2. Preview enhancements:
   ```bash
   mkdocs-ai enhance test-doc.md --grammar --clarity --preview
   ```

3. Apply enhancements:
   ```bash
   mkdocs-ai enhance test-doc.md --grammar --clarity --apply
   ```

**Expected Result**:
- Spelling errors fixed (Guid → Guide, platfrom → platform)
- Grammar improved (allow → allows, there → their)
- Clarity enhanced
- Original meaning preserved

**Report**:
- Errors correctly identified
- Fixes are appropriate
- No false positives
- Any issues

---

### Scenario 7: Asset Processing

**Goal**: Test automatic documentation from code.

**Steps**:

1. Process Python code:
   ```bash
   mkdocs-ai assets process \
     --type python \
     --path mkdocs_ai/cache \
     --output-dir docs/api
   ```

2. Check generated docs:
   ```bash
   ls docs/api/
   cat docs/api/manager.md
   ```

**Expected Result**:
- API documentation generated
- Includes class and function signatures
- Has AI-generated summaries
- Proper markdown formatting

**Report**:
- Documentation quality (1-5 stars)
- Completeness
- Any missing features
- Errors encountered

---

### Scenario 8: Obelisk Export

**Goal**: Test documentation export for RAG systems.

**Steps**:

1. Build a site (use Scenario 3)

2. Export to Obelisk format:
   ```bash
   mkdocs-ai obelisk export \
     --site-dir site \
     --site-url https://example.com \
     --output obelisk-export.json
   ```

3. Check export file:
   ```bash
   cat obelisk-export.json | jq '.document_count'
   ```

**Expected Result**:
- JSON file created
- Contains all pages
- Proper structure (id, title, content, url)
- Metadata included

**Report**:
- Export successful
- Document count matches site
- JSON structure valid
- Any issues

---

## Performance Testing

### Test 1: Generation Speed

Generate 10 documents and measure time:

```bash
for i in {1..10}; do
  time mkdocs-ai generate \
    "Create a guide about topic $i" \
    --output "test-$i.md"
done
```

**Report**:
- Average time per document: ___ seconds
- Total time: ___ seconds
- Cache hit rate: ___%

### Test 2: Build Time

Build a site with 50 pages:

```bash
time mkdocs build
```

**Report**:
- Build time: ___ seconds
- Pages processed: ___
- AI generations: ___
- Memory usage: ___ MB

### Test 3: Search Performance

Index 100 pages and measure query time:

```bash
time mkdocs-ai search build
time mkdocs-ai search query "test query"
```

**Report**:
- Index build time: ___ seconds
- Query time: ___ ms
- Index size: ___ MB

---

## Edge Cases to Test

### 1. Large Prompts

Test with very long prompts (>2000 words).

**Expected**: Should handle gracefully or show clear error.

### 2. Special Characters

Test with prompts containing:
- Unicode characters (emoji, non-Latin)
- Code snippets
- Markdown syntax

**Expected**: Should escape/handle properly.

### 3. Network Issues

Test with:
- No internet connection
- Slow connection
- Provider downtime

**Expected**: Clear error messages, retry logic works.

### 4. Invalid Configuration

Test with:
- Missing API key
- Invalid model name
- Wrong provider name

**Expected**: Validation errors, helpful messages.

### 5. Concurrent Requests

Run multiple generations simultaneously:

```bash
mkdocs-ai generate "Topic 1" --output t1.md &
mkdocs-ai generate "Topic 2" --output t2.md &
mkdocs-ai generate "Topic 3" --output t3.md &
wait
```

**Expected**: All complete successfully, no race conditions.

---

## Feedback Template

### General Feedback

**Overall Experience** (1-5 stars): ⭐⭐⭐⭐⭐

**What worked well**:
- 

**What needs improvement**:
- 

**Bugs encountered**:
- 

**Feature requests**:
- 

### Specific Feedback

**Installation** (Easy/Medium/Hard): 

**Documentation** (Clear/Unclear): 

**Performance** (Fast/Acceptable/Slow): 

**Output Quality** (Excellent/Good/Poor): 

**Would you use this in production?** (Yes/No/Maybe): 

**Additional comments**:


---

## Reporting Issues

### Bug Reports

Create an issue at: https://github.com/genpozi/mkdocs-ultra-material/issues

Include:
- Scenario being tested
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs
- System info (OS, Python version)

### Feature Requests

Create a discussion at: https://github.com/genpozi/mkdocs-ultra-material/discussions

Include:
- Use case description
- Proposed solution
- Why it's important
- Examples

---

## Known Issues

See [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for current limitations.

---

## Getting Help

- **Documentation**: Check README.md and docs/
- **Discussions**: GitHub Discussions
- **Issues**: GitHub Issues
- **Chat**: (Coming soon)

---

## Thank You! 🙏

Your feedback is invaluable for making MkDocs Ultra Material better. We appreciate your time and effort in testing!

**Happy Testing!**
