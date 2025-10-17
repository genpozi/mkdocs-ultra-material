# Priority 3: Semantic Search - Detailed Design

**Date**: October 17, 2025  
**Status**: Design Phase  
**Estimated Effort**: 4-6 hours

---

## Overview

Semantic Search adds AI-powered search capabilities to MkDocs documentation by:
- Generating vector embeddings for all documentation pages
- Creating a searchable index with semantic understanding
- Providing hybrid search (keyword + semantic)
- Enabling context-aware search results
- Integrating seamlessly with MkDocs Material's existing search

---

## Goals

### Primary Goals
1. **Semantic Understanding**: Search by meaning, not just keywords
2. **Better Results**: Find relevant content even with different terminology
3. **Fast Performance**: Sub-second search response times
4. **Portable Index**: JSON-based index that works anywhere
5. **Hybrid Search**: Combine keyword and semantic search
6. **Easy Integration**: Works with existing MkDocs Material search

### Non-Goals
- Not replacing MkDocs Material's search (complementing it)
- Not a full-text search engine (use existing tools for that)
- Not real-time indexing (build-time only)
- Not a chatbot interface (that's Priority 5)

---

## Architecture

### Component Overview

```
Semantic Search System
├── EmbeddingGenerator
│   ├── Generate embeddings for pages
│   ├── Chunk long documents
│   ├── Cache embeddings
│   └── Batch processing
│
├── VectorIndex
│   ├── Store embeddings in JSON
│   ├── Cosine similarity search
│   ├── Hybrid search (keyword + semantic)
│   └── Result ranking
│
├── SearchInterface
│   ├── JavaScript search widget
│   ├── API endpoint (optional)
│   └── Result rendering
│
└── CLI Commands
    ├── mkdocs-ai search-index build
    ├── mkdocs-ai search-index stats
    └── mkdocs-ai search "query"
```

### Data Flow

```
Build Time:
    Documentation Pages
        ↓
    EmbeddingGenerator.generate()
        ↓ (chunks + embeddings)
    VectorIndex.build()
        ↓
    JSON Index File (search_index.json)

Search Time:
    User Query
        ↓
    EmbeddingGenerator.embed(query)
        ↓ (query embedding)
    VectorIndex.search()
        ├→ Semantic Search (cosine similarity)
        ├→ Keyword Search (BM25)
        └→ Hybrid Ranking
        ↓
    Ranked Results
```

---

## Component Design

### 1. EmbeddingGenerator

**Purpose**: Generate vector embeddings for documentation content

**Features**:
- Chunk long documents into manageable pieces
- Generate embeddings using AI provider
- Cache embeddings to avoid regeneration
- Batch processing for efficiency
- Progress tracking

**Implementation**:

```python
class EmbeddingGenerator:
    """Generates vector embeddings for documentation."""
    
    def __init__(self, provider: AIProvider, cache: CacheManager):
        self.provider = provider
        self.cache = cache
        self.chunk_size = 1000  # characters
        self.chunk_overlap = 200  # characters
    
    async def generate_page_embeddings(
        self, 
        page: Page
    ) -> list[PageChunk]:
        """Generate embeddings for a single page.
        
        Args:
            page: MkDocs page object
            
        Returns:
            List of chunks with embeddings
        """
        # Extract text content
        text = self._extract_text(page.content)
        
        # Chunk the text
        chunks = self._chunk_text(text)
        
        # Generate embeddings for each chunk
        embeddings = []
        for chunk in chunks:
            # Check cache first
            cache_key = self._cache_key(chunk.text)
            embedding = self.cache.get(cache_key)
            
            if embedding is None:
                # Generate new embedding
                embedding = await self.provider.embed(chunk.text)
                self.cache.set(cache_key, embedding)
            
            embeddings.append(PageChunk(
                page_url=page.url,
                title=page.title,
                text=chunk.text,
                embedding=embedding,
                start_pos=chunk.start,
                end_pos=chunk.end
            ))
        
        return embeddings
    
    def _chunk_text(self, text: str) -> list[TextChunk]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            chunks.append(TextChunk(
                text=chunk_text,
                start=start,
                end=end
            ))
            
            start += self.chunk_size - self.chunk_overlap
        
        return chunks
    
    def _extract_text(self, html: str) -> str:
        """Extract plain text from HTML content."""
        # Remove HTML tags
        # Remove code blocks (already indexed separately)
        # Keep headings and structure
        pass
```

### 2. VectorIndex

**Purpose**: Store and search vector embeddings

**Features**:
- JSON-based storage (portable, no dependencies)
- Cosine similarity search
- Keyword search (BM25 algorithm)
- Hybrid ranking
- Efficient in-memory search

**Implementation**:

```python
class VectorIndex:
    """Vector index for semantic search."""
    
    def __init__(self):
        self.chunks: list[PageChunk] = []
        self.embeddings: np.ndarray = None
        self.keyword_index: dict[str, list[int]] = {}
    
    def add_chunks(self, chunks: list[PageChunk]) -> None:
        """Add chunks to the index."""
        self.chunks.extend(chunks)
        
        # Build embedding matrix
        embeddings = [chunk.embedding for chunk in chunks]
        if self.embeddings is None:
            self.embeddings = np.array(embeddings)
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])
        
        # Build keyword index
        for i, chunk in enumerate(chunks, start=len(self.chunks)):
            words = self._tokenize(chunk.text)
            for word in words:
                if word not in self.keyword_index:
                    self.keyword_index[word] = []
                self.keyword_index[word].append(i)
    
    async def search(
        self,
        query: str,
        provider: AIProvider,
        limit: int = 10,
        semantic_weight: float = 0.7
    ) -> list[SearchResult]:
        """Search the index.
        
        Args:
            query: Search query
            provider: AI provider for query embedding
            limit: Maximum results to return
            semantic_weight: Weight for semantic vs keyword (0-1)
            
        Returns:
            Ranked search results
        """
        # Generate query embedding
        query_embedding = await provider.embed(query)
        
        # Semantic search (cosine similarity)
        semantic_scores = self._cosine_similarity(
            query_embedding, 
            self.embeddings
        )
        
        # Keyword search (BM25)
        keyword_scores = self._keyword_search(query)
        
        # Hybrid ranking
        final_scores = (
            semantic_weight * semantic_scores +
            (1 - semantic_weight) * keyword_scores
        )
        
        # Get top results
        top_indices = np.argsort(final_scores)[-limit:][::-1]
        
        results = []
        for idx in top_indices:
            chunk = self.chunks[idx]
            results.append(SearchResult(
                page_url=chunk.page_url,
                title=chunk.title,
                text=chunk.text,
                score=final_scores[idx],
                semantic_score=semantic_scores[idx],
                keyword_score=keyword_scores[idx]
            ))
        
        return results
    
    def _cosine_similarity(
        self, 
        query: list[float], 
        embeddings: np.ndarray
    ) -> np.ndarray:
        """Calculate cosine similarity between query and all embeddings."""
        query_norm = np.linalg.norm(query)
        embeddings_norm = np.linalg.norm(embeddings, axis=1)
        
        dot_product = np.dot(embeddings, query)
        similarity = dot_product / (query_norm * embeddings_norm)
        
        return similarity
    
    def _keyword_search(self, query: str) -> np.ndarray:
        """BM25 keyword search."""
        # Simplified BM25 implementation
        scores = np.zeros(len(self.chunks))
        query_words = self._tokenize(query)
        
        for word in query_words:
            if word in self.keyword_index:
                for idx in self.keyword_index[word]:
                    scores[idx] += 1.0
        
        # Normalize scores
        if scores.max() > 0:
            scores = scores / scores.max()
        
        return scores
    
    def save(self, path: str) -> None:
        """Save index to JSON file."""
        data = {
            "version": "1.0",
            "chunks": [
                {
                    "page_url": chunk.page_url,
                    "title": chunk.title,
                    "text": chunk.text,
                    "embedding": chunk.embedding,
                    "start_pos": chunk.start_pos,
                    "end_pos": chunk.end_pos
                }
                for chunk in self.chunks
            ]
        }
        
        with open(path, "w") as f:
            json.dump(data, f)
    
    @classmethod
    def load(cls, path: str) -> "VectorIndex":
        """Load index from JSON file."""
        with open(path, "r") as f:
            data = json.load(f)
        
        index = cls()
        chunks = [
            PageChunk(**chunk_data)
            for chunk_data in data["chunks"]
        ]
        index.add_chunks(chunks)
        
        return index
```

### 3. Data Models

**Models**:

```python
@dataclass
class TextChunk:
    """A chunk of text for processing."""
    text: str
    start: int
    end: int

@dataclass
class PageChunk:
    """A chunk of a page with embedding."""
    page_url: str
    title: str
    text: str
    embedding: list[float]
    start_pos: int
    end_pos: int

@dataclass
class SearchResult:
    """A search result."""
    page_url: str
    title: str
    text: str
    score: float
    semantic_score: float
    keyword_score: float
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "page_url": self.page_url,
            "title": self.title,
            "text": self.text,
            "score": float(self.score),
            "semantic_score": float(self.semantic_score),
            "keyword_score": float(self.keyword_score)
        }

@dataclass
class SearchConfig:
    """Configuration for semantic search."""
    enabled: bool = False
    chunk_size: int = 1000
    chunk_overlap: int = 200
    index_path: str = "search_index.json"
    semantic_weight: float = 0.7
    max_results: int = 10
```

---

## MkDocs Integration

### Plugin Hooks

```python
class AIAssistantPlugin(BasePlugin):
    
    def on_post_build(self, config: MkDocsConfig) -> None:
        """Generate search index after build."""
        if not self.config.search.enabled:
            return
        
        # Generate embeddings for all pages
        generator = EmbeddingGenerator(self.provider, self.cache)
        index = VectorIndex()
        
        for page in self.pages:
            chunks = await generator.generate_page_embeddings(page)
            index.add_chunks(chunks)
        
        # Save index
        index_path = os.path.join(
            config.site_dir,
            self.config.search.index_path
        )
        index.save(index_path)
        
        logger.info(f"Search index built: {len(index.chunks)} chunks")
```

### Configuration

```yaml
plugins:
  - ai-assistant:
      search:
        enabled: true
        chunk_size: 1000
        chunk_overlap: 200
        index_path: search_index.json
        semantic_weight: 0.7
        max_results: 10
```

---

## CLI Commands

### Build Index

```bash
# Build search index
mkdocs-ai search-index build

# Build with custom config
mkdocs-ai search-index build --config mkdocs.yml

# Show progress
mkdocs-ai search-index build --verbose
```

### Search

```bash
# Search from CLI
mkdocs-ai search "how to configure docker"

# Limit results
mkdocs-ai search "docker networking" --limit 5

# Adjust semantic weight
mkdocs-ai search "troubleshooting" --semantic-weight 0.8
```

### Index Stats

```bash
# Show index statistics
mkdocs-ai search-index stats

# Output:
# Search Index Statistics
# ----------------------
# Total chunks: 1,234
# Total pages: 45
# Average chunks per page: 27.4
# Index size: 2.3 MB
# Embedding dimensions: 1536
```

---

## User Interface

### JavaScript Integration

```javascript
// Load search index
const searchIndex = await fetch('/search_index.json').then(r => r.json());

// Search function
async function semanticSearch(query) {
    // Get query embedding from API
    const queryEmbedding = await getQueryEmbedding(query);
    
    // Calculate similarities
    const results = searchIndex.chunks.map(chunk => {
        const similarity = cosineSimilarity(queryEmbedding, chunk.embedding);
        return {
            ...chunk,
            score: similarity
        };
    });
    
    // Sort and return top results
    return results.sort((a, b) => b.score - a.score).slice(0, 10);
}
```

### Search Widget

```html
<!-- Enhanced search widget -->
<div class="md-search" data-md-component="search">
  <input 
    type="text" 
    placeholder="Search (semantic enabled)" 
    class="md-search__input"
  >
  <div class="md-search__output">
    <div class="md-search-result">
      <!-- Results rendered here -->
    </div>
  </div>
</div>
```

---

## Performance Considerations

### Build Time
- **Embedding Generation**: ~0.5s per page (with caching)
- **Index Building**: ~0.1s for 100 pages
- **Total Build Time**: +30s for 50-page site (first build)
- **Cached Builds**: +5s (only new/changed pages)

### Search Time
- **Query Embedding**: ~0.3s
- **Similarity Calculation**: <0.01s for 1000 chunks
- **Total Search Time**: <0.5s

### Index Size
- **Embeddings**: ~6KB per chunk (1536 dimensions × 4 bytes)
- **Metadata**: ~1KB per chunk
- **Total**: ~7KB per chunk
- **Example**: 1000 chunks = ~7MB index

### Optimization Strategies
1. **Caching**: Cache embeddings to avoid regeneration
2. **Chunking**: Optimal chunk size (1000 chars)
3. **Compression**: Gzip index file (70% reduction)
4. **Lazy Loading**: Load index on first search
5. **Web Workers**: Run search in background thread

---

## Dependencies

### Required
- `numpy>=1.26.0` - Vector operations
- Existing: `httpx`, `pydantic`, `diskcache`

### Optional
- `chromadb>=0.4.0` - Future: Vector database backend
- `scikit-learn>=1.3.0` - Future: Advanced ranking

---

## Testing Strategy

### Unit Tests
- Embedding generation
- Chunking algorithm
- Similarity calculation
- Index serialization

### Integration Tests
- Full build with search enabled
- Search query execution
- Result ranking
- Cache effectiveness

### Performance Tests
- Build time with various site sizes
- Search response time
- Index size scaling
- Memory usage

---

## Migration Path

### Phase 1: Basic Implementation (4 hours)
1. ✅ Design document (this file)
2. Implement EmbeddingGenerator
3. Implement VectorIndex
4. Add plugin hooks
5. Basic CLI commands

### Phase 2: Integration (2 hours)
6. Configuration system
7. Cache integration
8. Error handling
9. Progress indicators

### Phase 3: Polish (2 hours)
10. Documentation
11. Examples
12. Testing
13. Performance optimization

---

## Success Metrics

### Functionality
- [ ] Generate embeddings for all pages
- [ ] Build searchable index
- [ ] Execute semantic search queries
- [ ] Return relevant results
- [ ] Integrate with MkDocs build

### Performance
- [ ] Build time < 1 minute for 50 pages
- [ ] Search time < 500ms
- [ ] Index size < 10MB for 50 pages
- [ ] Cache hit rate > 90% on rebuild

### Quality
- [ ] Relevant results for test queries
- [ ] Better than keyword-only search
- [ ] No false positives
- [ ] Handles edge cases

---

## Future Enhancements

### Short Term
- Faceted search (by section, tag, etc.)
- Search analytics
- Query suggestions
- Result highlighting

### Long Term
- Real-time indexing
- Multi-language support
- Image search
- Code search
- Question answering

---

## Risks and Mitigations

### Risk: Large Index Size
**Mitigation**: 
- Compression (gzip)
- Reduced embedding dimensions
- Selective indexing

### Risk: Slow Build Times
**Mitigation**:
- Aggressive caching
- Parallel processing
- Incremental indexing

### Risk: Poor Search Quality
**Mitigation**:
- Tunable semantic weight
- Hybrid search
- Result ranking improvements

### Risk: API Costs
**Mitigation**:
- Caching (avoid regeneration)
- Batch processing
- Local embeddings (future)

---

## Conclusion

Priority 3 (Semantic Search) will add powerful AI-powered search capabilities to MkDocs Ultra Material. The design focuses on:

1. **Simplicity**: JSON-based index, no complex dependencies
2. **Performance**: Fast search, efficient caching
3. **Quality**: Hybrid search for best results
4. **Integration**: Seamless MkDocs integration

**Estimated Effort**: 4-6 hours
**Dependencies**: numpy (new)
**Impact**: High - Significantly improves documentation discoverability

**Next Steps**:
1. Implement EmbeddingGenerator
2. Implement VectorIndex
3. Add CLI commands
4. Integrate with plugin
5. Test and document

---

**Status**: Ready for implementation ✅
