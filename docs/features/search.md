# Semantic Search

AI-powered search with vector embeddings for better results.

## Overview

Semantic search understands the meaning of queries, not just keywords. Find relevant content even when exact words don't match.

## Features

- **Vector Embeddings**: AI-generated embeddings for semantic understanding
- **Hybrid Search**: Combines semantic and keyword search
- **Smart Chunking**: Intelligent text segmentation
- **JSON Index**: Portable, no database required

## Usage

### Build Search Index

Generate embeddings for your documentation:

```bash
mkdocs-ai search build
```

### Search Documentation

Query your documentation:

```bash
mkdocs-ai search query "How do I configure Docker networking?"
```

### View Statistics

See index information:

```bash
mkdocs-ai search stats
```

## Configuration

```yaml
plugins:
  - mkdocs-ai:
      search:
        enabled: true
        chunk_size: 1000
        chunk_overlap: 200
        index_path: search_index.json
```

## How It Works

1. **Text Extraction**: Extract text from built HTML
2. **Chunking**: Split into overlapping chunks
3. **Embedding**: Generate vector embeddings
4. **Indexing**: Store in JSON format
5. **Search**: Hybrid semantic + keyword search

## Search Quality

### Semantic Understanding

Traditional search:
```
Query: "container networking"
Matches: Only pages with exact words "container" and "networking"
```

Semantic search:
```
Query: "container networking"
Matches: Pages about Docker networks, bridge mode, overlay networks, etc.
```

### Ranking

Results are ranked by:

1. **Semantic Similarity**: Cosine similarity of embeddings
2. **Keyword Match**: BM25 scoring
3. **Hybrid Score**: Weighted combination

## Best Practices

1. **Build after changes**: Rebuild index when docs change
2. **Tune chunk size**: Larger chunks for technical docs
3. **Use overlap**: Prevents context loss at boundaries
4. **Cache embeddings**: Enabled by default

## Examples

### Build and Search

```bash
# Build the index
mkdocs-ai search build

# Search for content
mkdocs-ai search query "troubleshooting Docker"

# View statistics
mkdocs-ai search stats
```

### Integration with MkDocs

The search index is built automatically during `mkdocs build` when enabled.

## Performance

- **Index Build**: ~1-2 seconds per page
- **Search Query**: <100ms
- **Index Size**: ~1-2MB per 100 pages

## Next Steps

- [Asset Processing](assets.md) - Generate docs from code
- [Document Generation](generation.md) - Create new documentation
