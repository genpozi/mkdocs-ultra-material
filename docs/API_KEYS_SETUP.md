# API Keys Setup Guide

This guide shows you how to configure API keys for MkDocs AI Assistant.

---

## Available API Keys

### OpenRouter (Primary - Recommended)
- **API Key**: `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`
- **Provider**: `openrouter`
- **Access**: Multiple AI models through one API
- **Cost**: Free models available

### Google Gemini (Alternative)
- **API Key**: `AIzaSyBMGIp07y55y96lqIPe6SehC5TJH82ZZ54`
- **Provider**: `gemini`
- **Access**: Google's Gemini models
- **Cost**: Free tier available

### Resend (Optional - Email)
- **API Key**: `re_ErwEoJSJ_37XrcroKByAcEd1dBzMTcuUN`
- **Purpose**: Email notifications (future feature)
- **Not required**: For documentation generation

---

## Recommended Free Models (OpenRouter)

These models are completely free to use:

1. **meta-llama/llama-4-maverick:free** (Recommended)
   - Fast and capable
   - Good for general documentation
   - No cost

2. **deepseek/deepseek-chat-v3-0324:free**
   - Excellent for technical content
   - Good fallback option
   - No cost

3. **z-ai/glm-4.5-air:free**
   - Fast responses
   - Good for simple tasks
   - No cost

4. **openai/gpt-oss-20b:free**
   - Smaller model
   - Very fast
   - No cost

---

## Setup Methods

### Method 1: Environment Variables (Recommended)

```bash
# Set for current session
export OPENROUTER_API_KEY=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
export GEMINI_API_KEY=AIzaSyBMGIp07y55y96lqIPe6SehC5TJH82ZZ54

# Or add to ~/.bashrc or ~/.zshrc for persistence
echo 'export OPENROUTER_API_KEY=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' >> ~/.bashrc
echo 'export GEMINI_API_KEY=AIzaSyBMGIp07y55y96lqIPe6SehC5TJH82ZZ54' >> ~/.bashrc
source ~/.bashrc
```

### Method 2: .env File

Create a `.env` file in your project root:

```bash
# .env
OPENROUTER_API_KEY=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
GEMINI_API_KEY=AIzaSyBMGIp07y55y96lqIPe6SehC5TJH82ZZ54
RESEND_API_KEY=re_ErwEoJSJ_37XrcroKByAcEd1dBzMTcuUN
```

Then load it:

```bash
# Load .env file
export $(cat .env | xargs)
```

### Method 3: MkDocs Configuration

Add to `mkdocs.yml`:

```yaml
plugins:
  - ai-assistant:
      provider:
        name: openrouter
        api_key: !ENV OPENROUTER_API_KEY
        model: meta-llama/llama-4-maverick:free
        fallback: deepseek/deepseek-chat-v3-0324:free
```

### Method 4: CLI Arguments

Pass directly to commands:

```bash
mkdocs-ai generate "Docker guide" \
  --provider openrouter \
  --api-key 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 \
  --model meta-llama/llama-4-maverick:free
```

---

## Configuration Examples

### Example 1: OpenRouter with Free Models

```yaml
plugins:
  - ai-assistant:
      enabled: true
      debug: false
      
      provider:
        name: openrouter
        api_key: !ENV OPENROUTER_API_KEY
        model: meta-llama/llama-4-maverick:free
        fallback: deepseek/deepseek-chat-v3-0324:free
        temperature: 0.7
        max_tokens: 4000
      
      cache:
        enabled: true
        dir: .ai-cache
        ttl: 86400
      
      generation:
        enabled: true
        output_dir: docs/generated
        cli_enabled: true
        markdown_syntax: true
      
      enhancement:
        enabled: true
        auto_enhance: false
        features:
          - grammar
          - clarity
      
      search:
        enabled: true
        chunk_size: 1000
        chunk_overlap: 200
        index_path: search_index.json
```

### Example 2: Google Gemini

```yaml
plugins:
  - ai-assistant:
      provider:
        name: gemini
        api_key: !ENV GEMINI_API_KEY
        model: gemini-pro
        temperature: 0.7
```

### Example 3: Multiple Providers

```yaml
plugins:
  - ai-assistant:
      provider:
        name: openrouter
        api_key: !ENV OPENROUTER_API_KEY
        model: meta-llama/llama-4-maverick:free
        # Fallback to Gemini if OpenRouter fails
        fallback: gemini
```

---

## Testing Your Setup

### Test 1: Generate Documentation

```bash
# Set API key
export OPENROUTER_API_KEY=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

# Generate test document
mkdocs-ai generate "Write a brief introduction to Docker" \
  --provider openrouter \
  --model meta-llama/llama-4-maverick:free \
  --verbose
```

Expected output:
```
✓ Generated: docs/generated/write-a-brief-introduction-to-docker.md
```

### Test 2: Build with MkDocs

```bash
cd tests/test_site
export OPENROUTER_API_KEY=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
mkdocs build --verbose
```

Expected output:
```
INFO    -  Building documentation...
INFO    -  Cache initialized at .ai-cache
INFO    -  Documentation built in X.XX seconds
```

### Test 3: Search Index

```bash
# Build search index
export OPENROUTER_API_KEY=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

mkdocs-ai search build \
  --config tests/test_site/mkdocs.yml \
  --provider openrouter \
  --verbose
```

### Test 4: Enhancement

```bash
# Enhance a document
export OPENROUTER_API_KEY=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

mkdocs-ai enhance docs/index.md \
  --preview \
  --grammar \
  --clarity \
  --provider openrouter
```

---

## Quick Start Script

Save this as `setup_api_keys.sh`:

```bash
#!/bin/bash
# Setup API keys for MkDocs AI Assistant

# Export API keys
export OPENROUTER_API_KEY=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
export GEMINI_API_KEY=AIzaSyBMGIp07y55y96lqIPe6SehC5TJH82ZZ54

# Test generation
echo "Testing document generation..."
mkdocs-ai generate "Test document" \
  --provider openrouter \
  --model meta-llama/llama-4-maverick:free

echo ""
echo "✅ API keys configured!"
echo ""
echo "Available commands:"
echo "  mkdocs-ai generate <prompt>     - Generate documentation"
echo "  mkdocs-ai enhance <file>        - Enhance content"
echo "  mkdocs-ai search build          - Build search index"
echo "  mkdocs-ai search query <query>  - Search documentation"
```

Make it executable:

```bash
chmod +x setup_api_keys.sh
./setup_api_keys.sh
```

---

## Troubleshooting

### Error: "API key required"

**Solution**: Set the environment variable:

```bash
export OPENROUTER_API_KEY=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
```

### Error: "Failed to initialize AI provider"

**Solution**: Check that the API key is correct and the provider name matches:

```yaml
provider:
  name: openrouter  # Must match the API key type
  api_key: !ENV OPENROUTER_API_KEY
```

### Error: "Model not found"

**Solution**: Use one of the free models:

```bash
--model meta-llama/llama-4-maverick:free
```

### Slow Generation

**Solution**: 
1. Enable caching (it's on by default)
2. Use a faster model like `openai/gpt-oss-20b:free`
3. Reduce `max_tokens` in configuration

### Rate Limiting

**Solution**:
1. Free models have rate limits
2. Wait a few seconds between requests
3. Use caching to avoid repeated requests
4. Consider using multiple providers as fallbacks

---

## Best Practices

### 1. Use Environment Variables

Don't hardcode API keys in configuration files:

```yaml
# ✅ Good
api_key: !ENV OPENROUTER_API_KEY

# ❌ Bad
api_key: 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
```

### 2. Enable Caching

Caching saves API calls and speeds up builds:

```yaml
cache:
  enabled: true
  dir: .ai-cache
  ttl: 86400  # 24 hours
```

### 3. Use Free Models

Start with free models for testing:

```yaml
model: meta-llama/llama-4-maverick:free
fallback: deepseek/deepseek-chat-v3-0324:free
```

### 4. Set Fallbacks

Configure fallback models for reliability:

```yaml
provider:
  model: meta-llama/llama-4-maverick:free
  fallback: deepseek/deepseek-chat-v3-0324:free
```

### 5. Monitor Usage

Check cache statistics:

```bash
mkdocs-ai cache-stats
```

---

## Security Notes

### ⚠️ Important

1. **Never commit API keys** to version control
2. **Add .env to .gitignore**
3. **Use environment variables** for production
4. **Rotate keys** if exposed
5. **Use separate keys** for development and production

### .gitignore

Add these lines to `.gitignore`:

```
.env
.env.local
*.key
*_key.txt
```

---

## Next Steps

1. ✅ Configure API keys (you're here!)
2. Test document generation
3. Build search index
4. Enhance existing content
5. Integrate into your workflow

See [QUICK_START.md](QUICK_START.md) for usage examples.

---

**Last Updated**: October 17, 2025
