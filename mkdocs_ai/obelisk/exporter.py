"""Documentation exporter for Obelisk."""

import logging
from pathlib import Path
from typing import List, Optional
from bs4 import BeautifulSoup

from .models import ObeliskDocument
from .client import ObeliskClient

log = logging.getLogger(__name__)


class DocumentationExporter:
    """Export MkDocs documentation to Obelisk format."""

    def __init__(
        self,
        site_dir: Path,
        site_url: str,
        client: Optional[ObeliskClient] = None,
    ):
        """Initialize documentation exporter.

        Args:
            site_dir: Path to built site directory
            site_url: Base URL of the site
            client: Optional Obelisk client for uploading
        """
        self.site_dir = Path(site_dir)
        self.site_url = site_url.rstrip("/")
        self.client = client

    def extract_documents(self) -> List[ObeliskDocument]:
        """Extract documents from built site.

        Returns:
            List of Obelisk documents
        """
        documents = []

        # Find all HTML files
        html_files = list(self.site_dir.rglob("*.html"))

        for html_file in html_files:
            try:
                doc = self._extract_document(html_file)
                if doc:
                    documents.append(doc)
            except Exception as e:
                log.warning(f"Failed to extract {html_file}: {e}")

        log.info(f"Extracted {len(documents)} documents")
        return documents

    def _extract_document(self, html_file: Path) -> Optional[ObeliskDocument]:
        """Extract a single document from HTML file.

        Args:
            html_file: Path to HTML file

        Returns:
            Obelisk document or None if extraction fails
        """
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")

        # Extract title
        title_tag = soup.find("title")
        title = title_tag.get_text() if title_tag else html_file.stem

        # Extract main content
        main_content = soup.find("main") or soup.find("article") or soup.find("body")
        if not main_content:
            return None

        # Remove script and style tags
        for tag in main_content.find_all(["script", "style", "nav", "footer"]):
            tag.decompose()

        # Get text content
        content = main_content.get_text(separator="\n", strip=True)

        # Generate URL
        relative_path = html_file.relative_to(self.site_dir)
        url = f"{self.site_url}/{relative_path}"

        # Generate document ID
        doc_id = str(relative_path).replace("/", "_").replace(".html", "")

        # Extract metadata
        metadata = {
            "source": "mkdocs",
            "file_path": str(relative_path),
        }

        # Extract description from meta tag
        description_tag = soup.find("meta", attrs={"name": "description"})
        if description_tag:
            metadata["description"] = description_tag.get("content", "")

        return ObeliskDocument(
            id=doc_id,
            title=title,
            content=content,
            url=url,
            metadata=metadata,
        )

    async def export_to_obelisk(
        self,
        documents: Optional[List[ObeliskDocument]] = None,
    ) -> List[str]:
        """Export documents to Obelisk.

        Args:
            documents: Optional list of documents (extracts if not provided)

        Returns:
            List of uploaded document IDs

        Raises:
            ValueError: If no client is configured
        """
        if not self.client:
            raise ValueError("No Obelisk client configured")

        if documents is None:
            documents = self.extract_documents()

        # Upload in batches
        batch_size = 50
        all_ids = []

        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            ids = await self.client.upload_documents(batch)
            all_ids.extend(ids)

        log.info(f"Exported {len(all_ids)} documents to Obelisk")
        return all_ids

    def save_export(self, output_file: Path, documents: Optional[List[ObeliskDocument]] = None):
        """Save documents to JSON file.

        Args:
            output_file: Path to output JSON file
            documents: Optional list of documents (extracts if not provided)
        """
        import json

        if documents is None:
            documents = self.extract_documents()

        data = {
            "site_url": self.site_url,
            "document_count": len(documents),
            "documents": [
                {
                    "id": doc.id,
                    "title": doc.title,
                    "content": doc.content,
                    "url": doc.url,
                    "metadata": doc.metadata,
                }
                for doc in documents
            ],
        }

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        log.info(f"Saved export to {output_file}")
