"""Clarity and readability enhancement."""

import difflib
from typing import Optional

from ..providers.base import AIProvider
from ..cache.manager import CacheManager
from .models import Change, ChangeType, EnhancementOptions


class ClarityEnhancer:
    """Enhance clarity and readability.
    
    Uses AI to improve:
    - Complex sentences → simpler alternatives
    - Ambiguous statements → clear statements
    - Passive voice → active voice (when appropriate)
    - Flow and transitions
    - Readability
    """
    
    SYSTEM_PROMPT = """You are a technical documentation editor focused on clarity and readability.

Your task is to improve readability while preserving:
- Technical accuracy and all information
- Professional tone
- Conciseness (don't add fluff)
- Meaning and intent

Improvements to make:
1. Simplify complex sentences
2. Clarify ambiguous statements
3. Improve flow and transitions
4. Use active voice when appropriate
5. Make technical concepts clearer

Rules:
1. Preserve all technical information
2. Don't add unnecessary words
3. Maintain professional tone
4. Don't change technical terms
5. Keep it concise

Return ONLY the improved text with no explanations or comments."""
    
    def __init__(self, provider: AIProvider, cache: CacheManager):
        """Initialize clarity enhancer.
        
        Args:
            provider: AI provider for enhancements
            cache: Cache manager for results
        """
        self.provider = provider
        self.cache = cache
    
    async def enhance(
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
        if not text.strip():
            return text, []
        
        # Check cache
        cache_key = f"clarity:{hash(text)}:{options.temperature}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached['enhanced'], [
                Change(**c) for c in cached['changes']
            ]
        
        # Build prompt
        prompt = self._build_prompt(text)
        
        # Call AI
        try:
            response = await self.provider.generate(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                temperature=options.temperature,
                max_tokens=options.max_tokens
            )
            
            enhanced = response.content.strip()
            
            # Detect changes
            changes = self._detect_changes(text, enhanced)
            
            # Cache result
            self.cache.set(cache_key, {
                'enhanced': enhanced,
                'changes': [
                    {
                        'type': c.type.value,
                        'line_number': c.line_number,
                        'original': c.original,
                        'enhanced': c.enhanced,
                        'reason': c.reason,
                        'confidence': c.confidence
                    }
                    for c in changes
                ]
            })
            
            return enhanced, changes
            
        except Exception as e:
            # On error, return original text
            print(f"Clarity enhancement error: {e}")
            return text, []
    
    def _build_prompt(self, text: str) -> str:
        """Build enhancement prompt.
        
        Args:
            text: Text to enhance
            
        Returns:
            Prompt string
        """
        return f"""Improve the clarity and readability of this technical documentation:

{text}

Make it clearer and easier to understand while preserving all information.
Return the improved text."""
    
    def _detect_changes(self, original: str, enhanced: str) -> list[Change]:
        """Detect what changed between original and enhanced text.
        
        Args:
            original: Original text
            enhanced: Enhanced text
            
        Returns:
            List of changes
        """
        if original == enhanced:
            return []
        
        changes: list[Change] = []
        
        # Use difflib to find differences at sentence level
        original_sentences = self._split_sentences(original)
        enhanced_sentences = self._split_sentences(enhanced)
        
        matcher = difflib.SequenceMatcher(
            None,
            original_sentences,
            enhanced_sentences
        )
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                # Sentences were changed
                orig_text = ' '.join(original_sentences[i1:i2])
                enh_text = ' '.join(enhanced_sentences[j1:j2])
                
                if orig_text != enh_text:
                    changes.append(Change(
                        type=ChangeType.CLARITY,
                        line_number=None,  # Sentence-level, not line-level
                        original=orig_text,
                        enhanced=enh_text,
                        reason=self._get_change_reason(orig_text, enh_text),
                        confidence=0.8
                    ))
        
        return changes
    
    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences.
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting (can be improved)
        import re
        
        # Split on sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Filter out empty sentences
        return [s.strip() for s in sentences if s.strip()]
    
    def _get_change_reason(self, original: str, enhanced: str) -> str:
        """Get human-readable reason for change.
        
        Args:
            original: Original text
            enhanced: Enhanced text
            
        Returns:
            Reason string
        """
        # Analyze the change to determine reason
        orig_len = len(original.split())
        enh_len = len(enhanced.split())
        
        if enh_len < orig_len:
            return "Simplified complex sentence"
        elif "which" in original.lower() and "which" not in enhanced.lower():
            return "Improved sentence structure"
        elif original.count(',') > enhanced.count(','):
            return "Reduced complexity"
        else:
            return "Improved clarity"
