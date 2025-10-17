"""Main asset processor orchestrator."""

import logging
from pathlib import Path
from typing import Optional

from mkdocs_ai.cache.manager import CacheManager
from mkdocs_ai.providers.base import AIProvider

from .base import AssetProcessor
from .models import Asset, Documentation

logger = logging.getLogger("mkdocs.plugins.ai-assistant.assets")


class AssetProcessorOrchestrator:
    """Orchestrates asset processing with multiple processors."""

    def __init__(
        self, provider: Optional[AIProvider] = None, cache: Optional[CacheManager] = None
    ):
        """Initialize orchestrator.

        Args:
            provider: AI provider for content generation
            cache: Cache manager
        """
        self.provider = provider
        self.cache = cache
        self.processors: dict[str, AssetProcessor] = {}

    def register_processor(self, asset_type: str, processor: AssetProcessor):
        """Register a processor for an asset type.

        Args:
            asset_type: Type of asset (e.g., 'python', 'docker-compose')
            processor: Processor instance
        """
        self.processors[asset_type] = processor
        logger.debug(f"Registered processor for {asset_type}")

    async def process_asset(self, asset: Asset) -> Optional[Documentation]:
        """Process an asset with the appropriate processor.

        Args:
            asset: Asset to process

        Returns:
            Generated documentation or None if no processor available
        """
        processor = self.processors.get(asset.type)
        if not processor:
            logger.warning(f"No processor registered for asset type: {asset.type}")
            return None

        try:
            logger.info(f"Processing {asset.type} asset: {asset.path}")
            documentation = await processor.process(asset)
            logger.info(f"Successfully processed {asset.path}")
            return documentation
        except Exception as e:
            logger.error(f"Failed to process {asset.path}: {e}")
            return None

    async def process_assets(self, assets: list[Asset]) -> list[Documentation]:
        """Process multiple assets.

        Args:
            assets: List of assets to process

        Returns:
            List of generated documentation
        """
        docs = []
        for asset in assets:
            doc = await self.process_asset(asset)
            if doc:
                docs.append(doc)
        return docs

    def save_documentation(
        self, documentation: Documentation, output_dir: str
    ) -> Path:
        """Save documentation to file.

        Args:
            documentation: Documentation to save
            output_dir: Output directory

        Returns:
            Path to saved file
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Determine filename
        if documentation.file_path:
            file_path = output_path / documentation.file_path
        else:
            # Generate filename from metadata
            title = documentation.metadata.get("title", "untitled")
            filename = title.lower().replace(" ", "-") + ".md"
            file_path = output_path / filename

        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        file_path.write_text(documentation.content)
        logger.info(f"Saved documentation to {file_path}")

        return file_path
