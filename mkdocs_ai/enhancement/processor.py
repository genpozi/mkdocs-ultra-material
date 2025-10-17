"""Main enhancement processor."""

import difflib
from typing import Optional

from ..providers.base import AIProvider
from ..cache.manager import CacheManager
from .models import (
    EnhancementOptions,
    EnhancementResult,
    EnhancementConfig,
    Change,
    ChangeType
)
from .preserver import ContentPreserver
from .grammar import GrammarEnhancer
from .clarity import ClarityEnhancer
from .consistency import ConsistencyChecker


class EnhancementProcessor:
    """Main enhancement coordinator.
    
    Coordinates the enhancement pipeline:
    1. Extract protected content
    2. Apply enhancements (grammar, clarity, consistency)
    3. Restore protected content
    4. Generate diff
    """
    
    def __init__(
        self,
        provider: AIProvider,
        cache: CacheManager,
        config: Optional[EnhancementConfig] = None
    ):
        """Initialize enhancement processor.
        
        Args:
            provider: AI provider for enhancements
            cache: Cache manager for results
            config: Enhancement configuration
        """
        self.provider = provider
        self.cache = cache
        self.config = config or EnhancementConfig()
        self.preserver = ContentPreserver()
    
    async def enhance(
        self,
        markdown: str,
        options: Optional[EnhancementOptions] = None
    ) -> EnhancementResult:
        """Enhance markdown content.
        
        Args:
            markdown: Original markdown content
            options: Enhancement options (uses config if not provided)
            
        Returns:
            Enhancement result with original, enhanced, diff, and changes
        """
        if options is None:
            options = self.config.get_options()
        
        # Clear previous placeholders
        self.preserver.clear()
        
        # Extract protected content
        prose = self.preserver.extract(markdown)
        
        # Apply enhancements
        enhanced = prose
        all_changes: list[Change] = []
        
        if options.grammar:
            enhanced, grammar_changes = await self._enhance_grammar(
                enhanced, options
            )
            all_changes.extend(grammar_changes)
        
        if options.clarity:
            enhanced, clarity_changes = await self._enhance_clarity(
                enhanced, options
            )
            all_changes.extend(clarity_changes)
        
        if options.consistency:
            enhanced, consistency_changes = await self._check_consistency(
                enhanced, options
            )
            all_changes.extend(consistency_changes)
        
        # Restore protected content
        enhanced = self.preserver.restore(enhanced)
        
        # Generate diff
        diff = self._generate_diff(markdown, enhanced)
        
        return EnhancementResult(
            original=markdown,
            enhanced=enhanced,
            diff=diff,
            changes=all_changes
        )
    
    async def _enhance_grammar(
        self,
        text: str,
        options: EnhancementOptions
    ) -> tuple[str, list[Change]]:
        """Enhance grammar and spelling.
        
        Args:
            text: Text to enhance
            options: Enhancement options
            
        Returns:
            Tuple of (enhanced text, list of changes)
        """
        enhancer = GrammarEnhancer(self.provider, self.cache)
        return await enhancer.enhance(text, options)
    
    async def _enhance_clarity(
        self,
        text: str,
        options: EnhancementOptions
    ) -> tuple[str, list[Change]]:
        """Enhance clarity and readability.
        
        Args:
            text: Text to enhance
            options: Enhancement options
            
        Returns:
            Tuple of (enhanced text, list of changes)
        """
        enhancer = ClarityEnhancer(self.provider, self.cache)
        return await enhancer.enhance(text, options)
    
    async def _check_consistency(
        self,
        text: str,
        options: EnhancementOptions
    ) -> tuple[str, list[Change]]:
        """Check terminology consistency.
        
        Args:
            text: Text to check
            options: Enhancement options (includes glossary)
            
        Returns:
            Tuple of (enhanced text, list of changes)
        """
        checker = ConsistencyChecker(
            self.provider,
            self.cache,
            options.glossary
        )
        return await checker.check(text, options)
    
    def _generate_diff(self, original: str, enhanced: str) -> str:
        """Generate unified diff.
        
        Args:
            original: Original content
            enhanced: Enhanced content
            
        Returns:
            Unified diff string
        """
        if original == enhanced:
            return ""
        
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            enhanced.splitlines(keepends=True),
            fromfile='original',
            tofile='enhanced',
            lineterm=''
        )
        
        return ''.join(diff)
    
    def get_preservation_stats(self) -> dict[str, int]:
        """Get statistics about preserved content.
        
        Returns:
            Dictionary with counts by content type
        """
        return self.preserver.get_stats()


class EnhancementPipeline:
    """High-level enhancement pipeline for batch processing."""
    
    def __init__(
        self,
        provider: AIProvider,
        cache: CacheManager,
        config: Optional[EnhancementConfig] = None
    ):
        """Initialize enhancement pipeline.
        
        Args:
            provider: AI provider
            cache: Cache manager
            config: Enhancement configuration
        """
        self.processor = EnhancementProcessor(provider, cache, config)
    
    async def enhance_file(
        self,
        file_path: str,
        options: Optional[EnhancementOptions] = None
    ) -> EnhancementResult:
        """Enhance a single file.
        
        Args:
            file_path: Path to markdown file
            options: Enhancement options
            
        Returns:
            Enhancement result
        """
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Enhance
        result = await self.processor.enhance(content, options)
        
        return result
    
    async def enhance_files(
        self,
        file_paths: list[str],
        options: Optional[EnhancementOptions] = None
    ) -> dict[str, EnhancementResult]:
        """Enhance multiple files.
        
        Args:
            file_paths: List of file paths
            options: Enhancement options
            
        Returns:
            Dictionary mapping file paths to results
        """
        results = {}
        
        for file_path in file_paths:
            result = await self.enhance_file(file_path, options)
            results[file_path] = result
        
        return results
    
    def apply_enhancement(
        self,
        file_path: str,
        result: EnhancementResult
    ) -> None:
        """Apply enhancement result to file.
        
        Args:
            file_path: Path to file
            result: Enhancement result to apply
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result.enhanced)
