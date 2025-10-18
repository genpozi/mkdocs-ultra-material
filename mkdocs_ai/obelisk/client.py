"""Obelisk API client."""

import httpx
import logging
from typing import List, Optional, Dict, Any
from .models import ObeliskDocument, ObeliskQuery, ObeliskResponse

log = logging.getLogger(__name__)


class ObeliskClient:
    """Client for Obelisk RAG chatbot API."""

    def __init__(
        self,
        service_url: str,
        api_key: Optional[str] = None,
        timeout: int = 30,
    ):
        """Initialize Obelisk client.

        Args:
            service_url: Base URL for Obelisk service
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
        """
        self.service_url = service_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

    async def upload_document(self, document: ObeliskDocument) -> str:
        """Upload a document to Obelisk.

        Args:
            document: Document to upload

        Returns:
            Document ID

        Raises:
            httpx.HTTPError: If upload fails
        """
        headers = self._get_headers()

        payload = {
            "id": document.id,
            "title": document.title,
            "content": document.content,
            "url": document.url,
            "metadata": document.metadata,
        }

        if document.embedding:
            payload["embedding"] = document.embedding

        response = await self.client.post(
            f"{self.service_url}/api/documents",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()

        result = response.json()
        log.info(f"Uploaded document: {document.id}")
        return result.get("id", document.id)

    async def upload_documents(self, documents: List[ObeliskDocument]) -> List[str]:
        """Upload multiple documents to Obelisk.

        Args:
            documents: List of documents to upload

        Returns:
            List of document IDs
        """
        headers = self._get_headers()

        payload = {
            "documents": [
                {
                    "id": doc.id,
                    "title": doc.title,
                    "content": doc.content,
                    "url": doc.url,
                    "metadata": doc.metadata,
                    "embedding": doc.embedding,
                }
                for doc in documents
            ]
        }

        response = await self.client.post(
            f"{self.service_url}/api/documents/batch",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()

        result = response.json()
        log.info(f"Uploaded {len(documents)} documents")
        return result.get("ids", [])

    async def query(self, query: ObeliskQuery) -> ObeliskResponse:
        """Query the Obelisk chatbot.

        Args:
            query: Query object

        Returns:
            Response from chatbot

        Raises:
            httpx.HTTPError: If query fails
        """
        headers = self._get_headers()

        payload = {
            "question": query.question,
            "context": query.context,
            "max_results": query.max_results,
        }

        response = await self.client.post(
            f"{self.service_url}/api/query",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()

        result = response.json()

        sources = [
            ObeliskDocument(
                id=doc["id"],
                title=doc["title"],
                content=doc["content"],
                url=doc["url"],
                metadata=doc.get("metadata", {}),
            )
            for doc in result.get("sources", [])
        ]

        return ObeliskResponse(
            answer=result["answer"],
            sources=sources,
            confidence=result.get("confidence", 0.0),
            metadata=result.get("metadata", {}),
        )

    async def delete_document(self, document_id: str) -> bool:
        """Delete a document from Obelisk.

        Args:
            document_id: ID of document to delete

        Returns:
            True if successful

        Raises:
            httpx.HTTPError: If deletion fails
        """
        headers = self._get_headers()

        response = await self.client.delete(
            f"{self.service_url}/api/documents/{document_id}",
            headers=headers,
        )
        response.raise_for_status()

        log.info(f"Deleted document: {document_id}")
        return True

    async def get_analytics(self) -> Dict[str, Any]:
        """Get analytics from Obelisk.

        Returns:
            Analytics data including common questions and gaps

        Raises:
            httpx.HTTPError: If request fails
        """
        headers = self._get_headers()

        response = await self.client.get(
            f"{self.service_url}/api/analytics",
            headers=headers,
        )
        response.raise_for_status()

        return response.json()

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication.

        Returns:
            Headers dictionary
        """
        headers = {"Content-Type": "application/json"}

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        return headers

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
