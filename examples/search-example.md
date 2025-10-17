# Semantic Search Example

This example demonstrates how to use the semantic search feature in MkDocs AI Assistant.

## Configuration

Add to your `mkdocs.yml`:

```yaml
plugins:
  - ai-assistant:
      provider:
        name: openrouter
        api_key: !ENV OPENROUTER_API_KEY
        model: anthropic/claude-3.5-sonnet
      
      cache:
        enabled: true
        dir: .ai-cache
        ttl: 86400
      
      search:
        enabled: true
        chunk_size: 1000
        chunk_overlap: 200
        index_path: search_index.json
        semantic_weight: 0.7
        max_results: 10
```

## Building the Search Index

### During MkDocs Build

The search index is automatically built when you run:

```bash
mkdocs build
```

The index will be saved to `site/search_index.json`.

### Using CLI

You can also build the index separately:

```bash
# Build search index
mkdocs-ai search build

# Build with custom config
mkdocs-ai search build --config mkdocs.yml

# Build with custom output path
mkdocs-ai search build --output site/search_index.json

# Show progress
mkdocs-ai search build --verbose
```

## Searching

### Using CLI

```bash
# Basic search
mkdocs-ai search query "how to configure docker"

# Limit results
mkdocs-ai search query "docker networking" --limit 5

# Adjust semantic weight (0-1)
# Higher = more semantic, lower = more keyword-based
mkdocs-ai search query "troubleshooting" --semantic-weight 0.8

# Use custom index
mkdocs-ai search query "api documentation" --index site/search_index.json
```

### Example Queries

```bash
# Semantic search finds related concepts
mkdocs-ai search query "container orchestration"
# Finds: Docker, Kubernetes, Docker Compose, etc.

# Works with natural language
mkdocs-ai search query "how do I fix connection errors"
# Finds: troubleshooting, networking, debugging, etc.

# Understands synonyms
mkdocs-ai search query "getting started"
# Finds: installation, setup, quick start, tutorial, etc.
```

## Index Statistics

View statistics about your search index:

```bash
mkdocs-ai search stats

# Output:
# Search Index Statistics
# ----------------------
# Total chunks: 1,234
# Total pages: 45
# Avg chunks per page: 27.4
# Total words: 45,678
# Avg words per chunk: 37.0
# Unique words: 3,456
```

## Configuration Options

### `chunk_size`
Maximum characters per chunk (default: 1000)
- Larger chunks: More context, fewer chunks, larger index
- Smaller chunks: More precise results, more chunks, smaller index

### `chunk_overlap`
Overlap between chunks in characters (default: 200)
- Prevents splitting related content
- Improves search quality at chunk boundaries

### `min_chunk_size`
Minimum chunk size to process (default: 100)
- Filters out very short chunks
- Reduces noise in search results

### `semantic_weight`
Weight for semantic vs keyword search (default: 0.7)
- 1.0 = Pure semantic search
- 0.5 = Equal weight
- 0.0 = Pure keyword search

### `max_results`
Maximum results to return (default: 10)

## Performance

### Build Time
- First build: ~0.5s per page (generating embeddings)
- Cached builds: ~0.1s per page (only new/changed pages)
- Example: 50-page site = ~25s first build, ~5s cached

### Search Time
- Query embedding: ~0.3s
- Similarity calculation: <0.01s for 1000 chunks
- Total: <0.5s per search

### Index Size
- ~7KB per chunk (embedding + metadata)
- Example: 1000 chunks = ~7MB index
- Compression: Use gzip for 70% reduction

## Integration with MkDocs Material

The semantic search index can be used alongside MkDocs Material's built-in search:

1. **Keyword Search**: Fast, exact matches
2. **Semantic Search**: Understands meaning, finds related content

You can implement a hybrid search interface that uses both.

## Troubleshooting

### Index Not Building

Check that:
- Search is enabled in config
- API key is set
- Provider is configured correctly
- Docs directory exists

### Poor Search Results

Try adjusting:
- `semantic_weight`: Increase for more semantic, decrease for more keyword
- `chunk_size`: Smaller chunks for more precise results
- `chunk_overlap`: Increase to capture more context

### Large Index Size

Reduce size by:
- Increasing `min_chunk_size`
- Increasing `chunk_size`
- Excluding certain pages
- Using compression (gzip)

## Advanced Usage

### Custom Search Interface

Load and use the index in JavaScript:

```javascript
// Load search index
const response = await fetch('/search_index.json');
const index = await response.json();

// Search function
async function search(query) {
    // Get query embedding from your API
    const queryEmbedding = await getQueryEmbedding(query);
    
    // Calculate similarities
    const results = index.chunks.map(chunk => {
        const similarity = cosineSimilarity(
            queryEmbedding, 
            chunk.embedding
        );
        return { ...chunk, score: similarity };
    });
    
    // Sort and return top results
    return results
        .sort((a, b) => b.score - a.score)
        .slice(0, 10);
}
```

### Programmatic Access

Use the search API in Python:

```python
from mkdocs_ai.search.index import VectorIndex
from mkdocs_ai.providers import get_provider

# Load index
index = VectorIndex.load("site/search_index.json")

# Initialize provider
provider = get_provider("openrouter", {
    "api_key": "your-key",
    "model": "anthropic/claude-3.5-sonnet"
})

# Search
results = await index.search(
    query="docker networking",
    provider=provider,
    limit=10,
    semantic_weight=0.7
)

# Process results
for result in results:
    print(f"{result.title}: {result.score:.3f}")
    print(f"  {result.text[:100]}...")
```

## Best Practices

1. **Cache Embeddings**: Enable caching to avoid regenerating embeddings
2. **Incremental Builds**: Use `mkdocs serve` for fast rebuilds during development
3. **Tune Weights**: Experiment with `semantic_weight` for your content
4. **Monitor Size**: Check index size and adjust chunk settings if needed
5. **Test Queries**: Try various queries to ensure good results

## Next Steps

- Implement search UI in your theme
- Add search analytics
- Experiment with different chunk sizes
- Try different semantic weights
- Integrate with MkDocs Material search
