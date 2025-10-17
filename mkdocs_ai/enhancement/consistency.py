"""Terminology consistency checking."""

import re
from typing import Optional

from ..providers.base import AIProvider
from ..cache.manager import CacheManager
from .models import Change, ChangeType, EnhancementOptions


class ConsistencyChecker:
    """Check and enforce terminology consistency.
    
    Ensures consistent use of technical terms across documentation:
    - Standardizes term variations (e.g., "k8s" → "Kubernetes")
    - Enforces capitalization (e.g., "docker" → "Docker")
    - Maintains glossary compliance
    """
    
    def __init__(
        self,
        provider: AIProvider,
        cache: CacheManager,
        glossary: Optional[dict[str, str]] = None
    ):
        """Initialize consistency checker.
        
        Args:
            provider: AI provider (for building glossary)
            cache: Cache manager
            glossary: Term mapping (variation → preferred)
        """
        self.provider = provider
        self.cache = cache
        self.glossary = glossary or {}
    
    async def check(
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
        if not text.strip():
            return text, []
        
        # Merge glossaries (options override instance)
        glossary = {**self.glossary, **options.glossary}
        
        if not glossary:
            # No glossary provided, try to build one
            glossary = await self._build_glossary(text)
        
        # Find and fix inconsistencies
        enhanced = text
        changes: list[Change] = []
        
        for variation, preferred in glossary.items():
            # Find all occurrences of the variation
            occurrences = self._find_term_occurrences(enhanced, variation)
            
            if occurrences:
                # Replace with preferred term
                enhanced = self._replace_term(enhanced, variation, preferred)
                
                # Record change
                changes.append(Change(
                    type=ChangeType.CONSISTENCY,
                    line_number=None,  # Could track line numbers if needed
                    original=variation,
                    enhanced=preferred,
                    reason=f"Standardize to '{preferred}'",
                    confidence=1.0  # High confidence for glossary matches
                ))
        
        return enhanced, changes
    
    async def _build_glossary(self, text: str) -> dict[str, str]:
        """Build terminology glossary from text using AI.
        
        Args:
            text: Text to analyze
            
        Returns:
            Glossary mapping variations to preferred terms
        """
        # Check cache
        cache_key = f"glossary:{hash(text)}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        prompt = f"""Analyze this technical documentation and identify technical terms that should be standardized.

{text}

Return a JSON object mapping term variations to their preferred standard forms.
Focus on:
- Product names (e.g., "k8s" → "Kubernetes", "docker" → "Docker")
- Technical terms with multiple spellings
- Capitalization inconsistencies

Example format:
{{
  "k8s": "Kubernetes",
  "K8s": "Kubernetes",
  "docker": "Docker",
  "DOCKER": "Docker",
  "api": "API",
  "rest api": "REST API"
}}

Return ONLY the JSON object, no explanations."""
        
        try:
            response = await self.provider.generate(
                prompt=prompt,
                temperature=0.1  # Very low for consistency
            )
            
            # Parse JSON response
            import json
            glossary = json.loads(response.content)
            
            # Cache result
            self.cache.set(cache_key, glossary)
            
            return glossary
            
        except Exception as e:
            print(f"Glossary building error: {e}")
            return {}
    
    def _find_term_occurrences(self, text: str, term: str) -> list[tuple[int, int]]:
        """Find all occurrences of a term in text.
        
        Args:
            text: Text to search
            term: Term to find
            
        Returns:
            List of (start, end) positions
        """
        occurrences: list[tuple[int, int]] = []
        
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(term) + r'\b'
        
        for match in re.finditer(pattern, text, re.IGNORECASE):
            occurrences.append((match.start(), match.end()))
        
        return occurrences
    
    def _replace_term(self, text: str, old_term: str, new_term: str) -> str:
        """Replace all occurrences of a term.
        
        Args:
            text: Text to modify
            old_term: Term to replace
            new_term: Replacement term
            
        Returns:
            Modified text
        """
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(old_term) + r'\b'
        
        # Replace with case preservation where possible
        def replace_with_case(match):
            matched_text = match.group(0)
            
            # If original is all caps, make replacement all caps
            if matched_text.isupper():
                return new_term.upper()
            # If original is title case, make replacement title case
            elif matched_text[0].isupper():
                return new_term.capitalize()
            # Otherwise use replacement as-is
            else:
                return new_term
        
        return re.sub(pattern, replace_with_case, text, flags=re.IGNORECASE)
    
    def add_term(self, variation: str, preferred: str) -> None:
        """Add a term to the glossary.
        
        Args:
            variation: Term variation
            preferred: Preferred standard form
        """
        self.glossary[variation] = preferred
    
    def remove_term(self, variation: str) -> None:
        """Remove a term from the glossary.
        
        Args:
            variation: Term variation to remove
        """
        self.glossary.pop(variation, None)
    
    def get_glossary(self) -> dict[str, str]:
        """Get current glossary.
        
        Returns:
            Glossary dictionary
        """
        return self.glossary.copy()
