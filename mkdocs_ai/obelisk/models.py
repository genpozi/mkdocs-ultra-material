"""Data models for Obelisk integration."""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class ObeliskDocument:
    """Document for Obelisk RAG system."""

    id: str
    title: str
    content: str
    url: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None


@dataclass
class ObeliskQuery:
    """Query for Obelisk chatbot."""

    question: str
    context: Optional[str] = None
    max_results: int = 5


@dataclass
class ObeliskResponse:
    """Response from Obelisk chatbot."""

    answer: str
    sources: List[ObeliskDocument]
    confidence: float
    metadata: Dict[str, Any]


@dataclass
class DocumentationGap:
    """Identified gap in documentation."""

    question: str
    frequency: int
    suggested_title: str
    suggested_content: Optional[str] = None
    priority: str = "medium"  # low, medium, high
