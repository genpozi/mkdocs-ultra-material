"""Vector index for semantic search."""

import json
import logging
import math
from collections import defaultdict
from pathlib import Path
from typing import Optional

from mkdocs_ai.providers.base import AIProvider
from mkdocs_ai.search.models import PageChunk, SearchResult

logger = logging.getLogger("mkdocs.plugins.ai-assistant.search")


class VectorIndex:
    """Vector index for semantic search."""

    def __init__(self):
        """Initialize empty index."""
        self.chunks: list[PageChunk] = []
        self.keyword_index: dict[str, list[int]] = defaultdict(list)
        self.doc_lengths: list[int] = []
        self.avg_doc_length: float = 0.0

    def add_chunks(self, chunks: list[PageChunk]) -> None:
        """Add chunks to the index.

        Args:
            chunks: List of page chunks to add
        """
        start_idx = len(self.chunks)
        self.chunks.extend(chunks)

        # Build keyword index
        for i, chunk in enumerate(chunks, start=start_idx):
            words = self._tokenize(chunk.text)
            self.doc_lengths.append(len(words))

            for word in set(words):  # Use set to count unique words
                self.keyword_index[word].append(i)

        # Update average document length
        if self.doc_lengths:
            self.avg_doc_length = sum(self.doc_lengths) / len(self.doc_lengths)

        logger.debug(f"Added {len(chunks)} chunks to index (total: {len(self.chunks)})")

    async def search(
        self,
        query: str,
        provider: AIProvider,
        limit: int = 10,
        semantic_weight: float = 0.7,
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
        if not self.chunks:
            logger.warning("Search index is empty")
            return []

        # Generate query embedding
        try:
            query_embedding = await provider.embed(query)
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {e}")
            # Fall back to keyword-only search
            semantic_weight = 0.0
            query_embedding = None

        # Calculate scores
        if query_embedding and semantic_weight > 0:
            semantic_scores = self._semantic_search(query_embedding)
        else:
            semantic_scores = [0.0] * len(self.chunks)

        if semantic_weight < 1.0:
            keyword_scores = self._keyword_search(query)
        else:
            keyword_scores = [0.0] * len(self.chunks)

        # Hybrid ranking
        final_scores = [
            semantic_weight * sem + (1 - semantic_weight) * kw
            for sem, kw in zip(semantic_scores, keyword_scores)
        ]

        # Get top results
        scored_indices = [
            (idx, score) for idx, score in enumerate(final_scores) if score > 0
        ]
        scored_indices.sort(key=lambda x: x[1], reverse=True)
        top_indices = scored_indices[:limit]

        # Build results
        results = []
        for idx, score in top_indices:
            chunk = self.chunks[idx]
            results.append(
                SearchResult(
                    page_url=chunk.page_url,
                    title=chunk.title,
                    text=chunk.text,
                    score=score,
                    semantic_score=semantic_scores[idx],
                    keyword_score=keyword_scores[idx],
                    section=chunk.section,
                )
            )

        logger.info(f"Search for '{query}' returned {len(results)} results")
        return results

    def _semantic_search(self, query_embedding: list[float]) -> list[float]:
        """Perform semantic search using cosine similarity.

        Args:
            query_embedding: Query embedding vector

        Returns:
            Similarity scores for each chunk
        """
        scores = []

        # Calculate query norm
        query_norm = math.sqrt(sum(x * x for x in query_embedding))

        for chunk in self.chunks:
            # Calculate cosine similarity
            dot_product = sum(
                q * e for q, e in zip(query_embedding, chunk.embedding)
            )
            embedding_norm = math.sqrt(sum(x * x for x in chunk.embedding))

            if query_norm > 0 and embedding_norm > 0:
                similarity = dot_product / (query_norm * embedding_norm)
                # Normalize to 0-1 range
                score = (similarity + 1) / 2
            else:
                score = 0.0

            scores.append(score)

        return scores

    def _keyword_search(self, query: str) -> list[float]:
        """Perform keyword search using BM25.

        Args:
            query: Search query

        Returns:
            BM25 scores for each chunk
        """
        # BM25 parameters
        k1 = 1.5  # Term frequency saturation
        b = 0.75  # Length normalization

        query_words = self._tokenize(query)
        scores = [0.0] * len(self.chunks)

        for word in query_words:
            if word not in self.keyword_index:
                continue

            # Document frequency
            df = len(self.keyword_index[word])
            # Inverse document frequency
            idf = math.log((len(self.chunks) - df + 0.5) / (df + 0.5) + 1.0)

            for doc_idx in self.keyword_index[word]:
                # Term frequency in document
                doc_words = self._tokenize(self.chunks[doc_idx].text)
                tf = doc_words.count(word)

                # Document length normalization
                doc_length = self.doc_lengths[doc_idx]
                norm = 1 - b + b * (doc_length / self.avg_doc_length)

                # BM25 score
                score = idf * (tf * (k1 + 1)) / (tf + k1 * norm)
                scores[doc_idx] += score

        # Normalize scores to 0-1 range
        if scores:
            max_score = max(scores)
            if max_score > 0:
                scores = [s / max_score for s in scores]

        return scores

    def _tokenize(self, text: str) -> list[str]:
        """Tokenize text into words.

        Args:
            text: Text to tokenize

        Returns:
            List of lowercase words
        """
        # Simple tokenization: lowercase, split on non-alphanumeric
        import re

        words = re.findall(r"\b\w+\b", text.lower())
        # Filter out very short words and numbers
        return [w for w in words if len(w) > 2 and not w.isdigit()]

    def save(self, path: str) -> None:
        """Save index to JSON file.

        Args:
            path: Path to save index
        """
        data = {
            "version": "1.0",
            "total_chunks": len(self.chunks),
            "chunks": [
                {
                    "page_url": chunk.page_url,
                    "title": chunk.title,
                    "text": chunk.text,
                    "embedding": chunk.embedding,
                    "start_pos": chunk.start_pos,
                    "end_pos": chunk.end_pos,
                    "section": chunk.section,
                }
                for chunk in self.chunks
            ],
        }

        # Ensure directory exists
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved search index to {path} ({len(self.chunks)} chunks)")

    @classmethod
    def load(cls, path: str) -> "VectorIndex":
        """Load index from JSON file.

        Args:
            path: Path to load index from

        Returns:
            Loaded vector index
        """
        with open(path, "r") as f:
            data = json.load(f)

        index = cls()
        chunks = [PageChunk(**chunk_data) for chunk_data in data["chunks"]]
        index.add_chunks(chunks)

        logger.info(f"Loaded search index from {path} ({len(chunks)} chunks)")
        return index

    def stats(self) -> dict:
        """Get index statistics.

        Returns:
            Dictionary of statistics
        """
        if not self.chunks:
            return {
                "total_chunks": 0,
                "total_pages": 0,
                "avg_chunks_per_page": 0,
                "total_words": 0,
                "avg_words_per_chunk": 0,
                "unique_words": 0,
            }

        # Count unique pages
        unique_pages = len(set(chunk.page_url for chunk in self.chunks))

        # Calculate statistics
        total_words = sum(self.doc_lengths)
        avg_words = total_words / len(self.chunks) if self.chunks else 0

        return {
            "total_chunks": len(self.chunks),
            "total_pages": unique_pages,
            "avg_chunks_per_page": len(self.chunks) / unique_pages if unique_pages else 0,
            "total_words": total_words,
            "avg_words_per_chunk": avg_words,
            "unique_words": len(self.keyword_index),
        }
