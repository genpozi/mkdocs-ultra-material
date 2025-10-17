"""Data models for semantic search."""

from dataclasses import dataclass, field
from typing import Optional


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
    section: Optional[str] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class SearchResult:
    """A search result."""

    page_url: str
    title: str
    text: str
    score: float
    semantic_score: float
    keyword_score: float
    section: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "page_url": self.page_url,
            "title": self.title,
            "text": self.text,
            "score": float(self.score),
            "semantic_score": float(self.semantic_score),
            "keyword_score": float(self.keyword_score),
            "section": self.section,
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
    min_chunk_size: int = 100
