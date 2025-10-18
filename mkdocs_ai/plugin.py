"""Main MkDocs AI Assistant plugin."""

import asyncio
import logging
from pathlib import Path
from mkdocs.plugins import BasePlugin
from mkdocs.config.defaults import MkDocsConfig

from .config import AIAssistantConfig
from .providers import get_provider, ProviderError
from .cache import CacheManager
from .generation.markdown import MarkdownProcessor
from .search.embeddings import EmbeddingGenerator
from .search.index import VectorIndex

log = logging.getLogger("mkdocs.plugins.mkdocs-ai")


class AIAssistantPlugin(BasePlugin[AIAssistantConfig]):
    """MkDocs AI Assistant plugin for document generation and enhancement.
    
    This plugin provides AI-powered features for MkDocs documentation:
    - Document generation from prompts
    - Content enhancement (grammar, clarity, consistency)
    - Semantic search with embeddings
    - Asset-to-documentation conversion
    - Obelisk integration for RAG chatbot
    """

    def __init__(self):
        super().__init__()
        self.provider = None
        self.cache_manager = None
        self.markdown_processor = None
        self.is_serve = False
        self.pages_for_search = []

    def on_startup(self, *, command: str, dirty: bool) -> None:
        """Initialize plugin on MkDocs startup.
        
        Args:
            command: The MkDocs command being run
            dirty: Whether dirty build is enabled
        """
        self.is_serve = command == "serve"
        
        if self.config.debug:
            log.setLevel(logging.DEBUG)
            log.debug("AI Assistant plugin starting in debug mode")

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        """Initialize AI provider and cache on config load.
        
        Args:
            config: MkDocs configuration
            
        Returns:
            Modified MkDocs configuration
        """
        if not self.config.enabled:
            log.info("AI Assistant plugin is disabled")
            return config
        
        # Initialize cache manager
        if self.config.cache.enabled:
            try:
                self.cache_manager = CacheManager(
                    cache_dir=self.config.cache.dir,
                    ttl=self.config.cache.ttl,
                    max_size=self.config.cache.max_size,
                )
                log.info(f"Cache initialized at {self.config.cache.dir}")
            except Exception as e:
                log.warning(f"Failed to initialize cache: {e}")
                self.cache_manager = None
        
        # Initialize AI provider
        try:
            provider_config = {
                "name": self.config.provider.name,
                "api_key": self.config.provider.api_key,
                "base_url": self.config.provider.base_url,
                "model": self.config.provider.model,
                "fallback": self.config.provider.fallback,
                "temperature": self.config.provider.temperature,
                "max_tokens": self.config.provider.max_tokens,
                "timeout": self.config.provider.timeout,
            }
            
            self.provider = get_provider(provider_config)
            self.provider.validate_config()
            
            log.info(
                f"AI provider initialized: {self.config.provider.name} "
                f"(model: {self.config.provider.model})"
            )
            
        except ProviderError as e:
            log.error(f"Failed to initialize AI provider: {e}")
            log.warning("AI features will be disabled")
            self.provider = None
        except Exception as e:
            log.error(f"Unexpected error initializing provider: {e}")
            self.provider = None
        
        # Initialize markdown processor if generation enabled
        if self.provider and self.config.generation.enabled:
            if self.config.generation.markdown_syntax:
                self.markdown_processor = MarkdownProcessor(
                    provider=self.provider,
                    cache_manager=self.cache_manager,
                )
                log.info("Markdown syntax processing enabled")
        
        return config

    def on_pre_build(self, *, config: MkDocsConfig) -> None:
        """Run pre-build tasks.
        
        Args:
            config: MkDocs configuration
        """
        if not self.config.enabled or not self.provider:
            return
        
        log.info("AI Assistant pre-build phase")
        
        # TODO: Process generation tasks from config
        # TODO: Process asset sources
        
        if self.config.debug:
            log.debug(f"Generation enabled: {self.config.generation.enabled}")
            log.debug(f"Enhancement enabled: {self.config.enhancement.enabled}")
            log.debug(f"Search enabled: {self.config.search.enabled}")
            log.debug(f"Assets enabled: {self.config.assets.enabled}")

    def on_page_markdown(
        self,
        markdown: str,
        *,
        page,
        config: MkDocsConfig,
        files,
    ) -> str:
        """Process markdown content with AI.
        
        This hook handles:
        - AI-GENERATE comments for inline generation
        - Content enhancement if enabled
        
        Args:
            markdown: Page markdown content
            page: Page object
            config: MkDocs configuration
            files: Files collection
            
        Returns:
            Processed markdown content
        """
        if not self.config.enabled or not self.provider:
            return markdown
        
        # Process AI-GENERATE comments
        if self.markdown_processor:
            if self.markdown_processor.has_ai_comments(markdown):
                page_context = {
                    "title": page.title if hasattr(page, "title") else None,
                    "path": page.file.src_path if hasattr(page, "file") else None,
                }
                
                log.info(f"Processing AI comments in {page.file.src_path}")
                
                # Run async processing
                try:
                    markdown = asyncio.run(
                        self.markdown_processor.process_markdown(
                            markdown,
                            page_context,
                        )
                    )
                except Exception as e:
                    log.error(f"Failed to process AI comments: {e}")
        
        # TODO: Apply content enhancement if enabled
        
        # Collect page for search indexing
        if self.config.search.enabled:
            self.pages_for_search.append({
                "url": page.url if hasattr(page, "url") else page.file.url,
                "title": page.title if hasattr(page, "title") else page.file.name,
                "content": markdown,
            })
        
        return markdown

    def on_post_build(self, *, config: MkDocsConfig) -> None:
        """Run post-build tasks.
        
        Args:
            config: MkDocs configuration
        """
        if not self.config.enabled:
            return
        
        log.info("AI Assistant post-build phase")
        
        # Generate semantic search index
        if self.config.search.enabled and self.pages_for_search:
            log.info("Building semantic search index...")
            try:
                asyncio.run(self._build_search_index(config))
            except Exception as e:
                log.error(f"Failed to build search index: {e}")
        
        # TODO: Export to Obelisk format if enabled
        
        # Log cache statistics
        if self.cache_manager:
            stats = self.cache_manager.get_stats()
            log.info(
                f"Cache stats: {stats['count']} entries, "
                f"{stats['size'] / 1024 / 1024:.2f}MB, "
                f"{stats['hits']} hits, {stats['misses']} misses"
            )

    async def _build_search_index(self, config: MkDocsConfig) -> None:
        """Build semantic search index.
        
        Args:
            config: MkDocs configuration
        """
        # Initialize embedding generator
        generator = EmbeddingGenerator(
            provider=self.provider,
            cache=self.cache_manager,
            chunk_size=self.config.search.chunk_size,
            chunk_overlap=self.config.search.chunk_overlap,
            min_chunk_size=self.config.search.min_chunk_size,
        )
        
        # Initialize index
        index = VectorIndex()
        
        # Process all pages
        total_chunks = 0
        for page_data in self.pages_for_search:
            try:
                chunks = await generator.generate_page_embeddings(
                    page_url=page_data["url"],
                    page_title=page_data["title"],
                    page_content=page_data["content"],
                )
                index.add_chunks(chunks)
                total_chunks += len(chunks)
            except Exception as e:
                log.error(f"Failed to process page {page_data['url']}: {e}")
        
        # Save index
        index_path = Path(config.site_dir) / self.config.search.index_path
        index.save(str(index_path))
        
        log.info(
            f"Search index built: {total_chunks} chunks from "
            f"{len(self.pages_for_search)} pages"
        )

    def on_shutdown(self) -> None:
        """Clean up resources on shutdown."""
        if self.cache_manager:
            self.cache_manager.close()
            log.debug("Cache manager closed")
