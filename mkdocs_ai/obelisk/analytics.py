"""Analytics for documentation gaps and improvements."""

import logging
from typing import List, Dict, Any
from collections import Counter
from .models import DocumentationGap
from .client import ObeliskClient

log = logging.getLogger(__name__)


class DocumentationAnalytics:
    """Analyze documentation gaps and suggest improvements."""

    def __init__(self, client: ObeliskClient):
        """Initialize analytics.

        Args:
            client: Obelisk client for fetching data
        """
        self.client = client

    async def identify_gaps(self, min_frequency: int = 3) -> List[DocumentationGap]:
        """Identify documentation gaps from user questions.

        Args:
            min_frequency: Minimum question frequency to consider

        Returns:
            List of identified gaps
        """
        analytics = await self.client.get_analytics()

        # Get common questions
        questions = analytics.get("common_questions", [])

        # Get existing documents
        existing_topics = set(analytics.get("document_topics", []))

        gaps = []

        # Count question topics
        question_topics = Counter()
        for q in questions:
            topic = self._extract_topic(q["question"])
            if topic and topic not in existing_topics:
                question_topics[topic] += q.get("count", 1)

        # Create gap objects
        for topic, frequency in question_topics.items():
            if frequency >= min_frequency:
                gap = DocumentationGap(
                    question=topic,
                    frequency=frequency,
                    suggested_title=self._generate_title(topic),
                    priority=self._calculate_priority(frequency),
                )
                gaps.append(gap)

        # Sort by priority and frequency
        gaps.sort(key=lambda x: (x.priority, x.frequency), reverse=True)

        log.info(f"Identified {len(gaps)} documentation gaps")
        return gaps

    async def get_improvement_suggestions(self) -> List[Dict[str, Any]]:
        """Get suggestions for improving existing documentation.

        Returns:
            List of improvement suggestions
        """
        analytics = await self.client.get_analytics()

        suggestions = []

        # Low confidence answers indicate unclear documentation
        low_confidence = analytics.get("low_confidence_queries", [])
        for query in low_confidence:
            suggestions.append(
                {
                    "type": "clarity",
                    "document_id": query.get("document_id"),
                    "issue": "Low confidence answers",
                    "suggestion": "Improve clarity and add more details",
                    "priority": "high",
                }
            )

        # Frequently asked questions about existing docs
        frequent_questions = analytics.get("frequent_questions", [])
        for q in frequent_questions:
            if q.get("has_answer") and q.get("count", 0) > 10:
                suggestions.append(
                    {
                        "type": "faq",
                        "question": q["question"],
                        "suggestion": "Add to FAQ or troubleshooting section",
                        "priority": "medium",
                    }
                )

        log.info(f"Generated {len(suggestions)} improvement suggestions")
        return suggestions

    def _extract_topic(self, question: str) -> str:
        """Extract topic from question.

        Args:
            question: User question

        Returns:
            Extracted topic
        """
        # Simple topic extraction - can be enhanced with NLP
        question = question.lower()

        # Remove common question words
        for word in ["how", "what", "why", "when", "where", "can", "do", "does"]:
            question = question.replace(word, "")

        # Clean up
        topic = " ".join(question.split())
        return topic

    def _generate_title(self, topic: str) -> str:
        """Generate documentation title from topic.

        Args:
            topic: Topic string

        Returns:
            Suggested title
        """
        # Capitalize and format
        words = topic.split()
        title = " ".join(word.capitalize() for word in words)
        return title

    def _calculate_priority(self, frequency: int) -> str:
        """Calculate priority based on frequency.

        Args:
            frequency: Question frequency

        Returns:
            Priority level (low, medium, high)
        """
        if frequency >= 10:
            return "high"
        elif frequency >= 5:
            return "medium"
        else:
            return "low"
