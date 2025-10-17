"""Embedding generation for semantic search."""

import hashlib
import logging
import re
from html.parser import HTMLParser
from typing import Optional

from mkdocs_ai.cache.manager import CacheManager
from mkdocs_ai.providers.base import AIProvider
from mkdocs_ai.search.models import PageChunk, TextChunk

logger = logging.getLogger("mkdocs.plugins.ai-assistant.search")


class HTMLTextExtractor(HTMLParser):
    """Extract plain text from HTML."""

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {"script", "style", "code", "pre"}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        """Handle opening tags."""
        self.current_tag = tag

    def handle_endtag(self, tag):
        """Handle closing tags."""
        self.current_tag = None

    def handle_data(self, data):
        """Handle text data."""
        if self.current_tag not in self.skip_tags:
            # Clean up whitespace
            text = " ".join(data.split())
            if text:
                self.text_parts.append(text)

    def get_text(self) -> str:
        """Get extracted text."""
        return " ".join(self.text_parts)


class EmbeddingGenerator:
    """Generates vector embeddings for documentation."""

    def __init__(
        self,
        provider: AIProvider,
        cache: Optional[CacheManager] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        min_chunk_size: int = 100,
    ):
        """Initialize embedding generator.

        Args:
            provider: AI provider for generating embeddings
            cache: Cache manager for storing embeddings
            chunk_size: Maximum characters per chunk
            chunk_overlap: Overlap between chunks
            min_chunk_size: Minimum chunk size to process
        """
        self.provider = provider
        self.cache = cache
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size

    async def generate_page_embeddings(
        self, page_url: str, page_title: str, page_content: str
    ) -> list[PageChunk]:
        """Generate embeddings for a single page.

        Args:
            page_url: URL of the page
            page_title: Title of the page
            page_content: HTML content of the page

        Returns:
            List of chunks with embeddings
        """
        # Extract plain text from HTML
        text = self._extract_text(page_content)

        if not text or len(text) < self.min_chunk_size:
            logger.debug(f"Skipping page {page_url}: too short ({len(text)} chars)")
            return []

        # Chunk the text
        chunks = self._chunk_text(text)

        logger.debug(f"Processing {len(chunks)} chunks for {page_url}")

        # Generate embeddings for each chunk
        page_chunks = []
        for i, chunk in enumerate(chunks):
            # Check cache first
            cache_key = self._cache_key(chunk.text)
            embedding = None

            if self.cache:
                embedding = self.cache.get(cache_key)

            if embedding is None:
                # Generate new embedding
                try:
                    embedding = await self.provider.embed(chunk.text)

                    # Cache the embedding
                    if self.cache:
                        self.cache.set(cache_key, embedding)

                    logger.debug(f"Generated embedding for chunk {i+1}/{len(chunks)}")
                except Exception as e:
                    logger.error(f"Failed to generate embedding for chunk: {e}")
                    continue

            # Extract section from chunk (first heading)
            section = self._extract_section(chunk.text)

            page_chunks.append(
                PageChunk(
                    page_url=page_url,
                    title=page_title,
                    text=chunk.text,
                    embedding=embedding,
                    start_pos=chunk.start,
                    end_pos=chunk.end,
                    section=section,
                )
            )

        logger.info(
            f"Generated {len(page_chunks)} embeddings for {page_url} "
            f"({len(text)} chars)"
        )

        return page_chunks

    def _extract_text(self, html: str) -> str:
        """Extract plain text from HTML content.

        Args:
            html: HTML content

        Returns:
            Plain text with structure preserved
        """
        parser = HTMLTextExtractor()
        parser.feed(html)
        return parser.get_text()

    def _chunk_text(self, text: str) -> list[TextChunk]:
        """Split text into overlapping chunks.

        Args:
            text: Text to chunk

        Returns:
            List of text chunks
        """
        chunks = []
        start = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))

            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence ending
                sentence_end = self._find_sentence_boundary(text, end)
                if sentence_end > start + self.min_chunk_size:
                    end = sentence_end

            chunk_text = text[start:end].strip()

            if len(chunk_text) >= self.min_chunk_size:
                chunks.append(TextChunk(text=chunk_text, start=start, end=end))

            # Move to next chunk with overlap
            start = end - self.chunk_overlap

            # Avoid infinite loop
            if start >= len(text):
                break

        return chunks

    def _find_sentence_boundary(self, text: str, pos: int) -> int:
        """Find the nearest sentence boundary.

        Args:
            text: Text to search
            pos: Starting position

        Returns:
            Position of sentence boundary
        """
        # Look for sentence endings within 100 chars
        search_start = max(0, pos - 100)
        search_end = min(len(text), pos + 100)
        search_text = text[search_start:search_end]

        # Find last sentence ending before pos
        for pattern in [r"\.\s+", r"\!\s+", r"\?\s+", r"\n\n"]:
            matches = list(re.finditer(pattern, search_text))
            if matches:
                # Get last match before relative position
                rel_pos = pos - search_start
                for match in reversed(matches):
                    if match.end() <= rel_pos:
                        return search_start + match.end()

        return pos

    def _extract_section(self, text: str) -> Optional[str]:
        """Extract section name from chunk text.

        Args:
            text: Chunk text

        Returns:
            Section name if found
        """
        # Look for markdown-style headings at start
        lines = text.split("\n", 3)
        for line in lines[:3]:
            line = line.strip()
            if line.startswith("#"):
                # Remove # symbols
                return line.lstrip("#").strip()

        return None

    def _cache_key(self, text: str) -> str:
        """Generate cache key for text.

        Args:
            text: Text to generate key for

        Returns:
            Cache key
        """
        # Use hash of text as cache key
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        return f"embedding:{text_hash[:16]}"
