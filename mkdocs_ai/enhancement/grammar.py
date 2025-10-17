"""Grammar and spelling enhancement."""

import difflib
from typing import Optional

from ..providers.base import AIProvider
from ..cache.manager import CacheManager
from .models import Change, ChangeType, EnhancementOptions


class GrammarEnhancer:
    """Enhance grammar and spelling.
    
    Uses AI to fix:
    - Grammar errors
    - Spelling mistakes
    - Punctuation issues
    - Sentence structure (only if grammatically incorrect)
    """
    
    SYSTEM_PROMPT = """You are a technical documentation editor specializing in grammar and spelling.

Your task is to fix grammar and spelling errors while preserving:
- Technical terminology (even if it looks unusual)
- Meaning and intent
- Writing style and tone
- Sentence structure (unless grammatically incorrect)
- All information and details

Rules:
1. Only fix clear errors - do not rewrite or restructure
2. Preserve technical terms exactly as written
3. Do not change code, commands, or technical syntax
4. Do not add or remove information
5. Maintain the original voice and style

Return ONLY the corrected text with no explanations or comments."""
    
    def __init__(self, provider: AIProvider, cache: CacheManager):
        """Initialize grammar enhancer.
        
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
        """Enhance grammar and spelling.
        
        Args:
            text: Text to enhance
            options: Enhancement options
            
        Returns:
            Tuple of (enhanced text, list of changes)
        """
        if not text.strip():
            return text, []
        
        # Check cache
        cache_key = f"grammar:{hash(text)}:{options.temperature}"
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
            print(f"Grammar enhancement error: {e}")
            return text, []
    
    def _build_prompt(self, text: str) -> str:
        """Build enhancement prompt.
        
        Args:
            text: Text to enhance
            
        Returns:
            Prompt string
        """
        return f"""Fix grammar and spelling errors in this technical documentation:

{text}

Return the corrected text."""
    
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
        
        # Use difflib to find differences
        original_lines = original.splitlines()
        enhanced_lines = enhanced.splitlines()
        
        matcher = difflib.SequenceMatcher(None, original_lines, enhanced_lines)
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                # Lines were changed
                for line_num in range(i1, i2):
                    if line_num < len(original_lines) and line_num < len(enhanced_lines):
                        orig_line = original_lines[line_num]
                        enh_line = enhanced_lines[line_num]
                        
                        if orig_line != enh_line:
                            # Detect specific changes within the line
                            word_changes = self._detect_word_changes(
                                orig_line, enh_line, line_num + 1
                            )
                            changes.extend(word_changes)
            
            elif tag == 'delete':
                # Lines were deleted (shouldn't happen with grammar fixes)
                pass
            
            elif tag == 'insert':
                # Lines were inserted (shouldn't happen with grammar fixes)
                pass
        
        return changes
    
    def _detect_word_changes(
        self,
        original_line: str,
        enhanced_line: str,
        line_number: int
    ) -> list[Change]:
        """Detect word-level changes in a line.
        
        Args:
            original_line: Original line
            enhanced_line: Enhanced line
            line_number: Line number
            
        Returns:
            List of changes
        """
        changes: list[Change] = []
        
        # Split into words
        orig_words = original_line.split()
        enh_words = enhanced_line.split()
        
        # Use sequence matcher for words
        matcher = difflib.SequenceMatcher(None, orig_words, enh_words)
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                # Words were changed
                orig_text = ' '.join(orig_words[i1:i2])
                enh_text = ' '.join(enh_words[j1:j2])
                
                # Determine change type
                change_type = self._classify_change(orig_text, enh_text)
                
                changes.append(Change(
                    type=change_type,
                    line_number=line_number,
                    original=orig_text,
                    enhanced=enh_text,
                    reason=self._get_change_reason(change_type, orig_text, enh_text),
                    confidence=0.9
                ))
        
        return changes
    
    def _classify_change(self, original: str, enhanced: str) -> ChangeType:
        """Classify the type of change.
        
        Args:
            original: Original text
            enhanced: Enhanced text
            
        Returns:
            Change type
        """
        # Simple heuristics for classification
        orig_lower = original.lower()
        enh_lower = enhanced.lower()
        
        # Check if it's a spelling change (same length, similar)
        if len(original) == len(enhanced) and orig_lower != enh_lower:
            return ChangeType.SPELLING
        
        # Check if it's punctuation
        if original.strip('.,;:!?') == enhanced.strip('.,;:!?'):
            return ChangeType.GRAMMAR
        
        # Default to grammar
        return ChangeType.GRAMMAR
    
    def _get_change_reason(
        self,
        change_type: ChangeType,
        original: str,
        enhanced: str
    ) -> str:
        """Get human-readable reason for change.
        
        Args:
            change_type: Type of change
            original: Original text
            enhanced: Enhanced text
            
        Returns:
            Reason string
        """
        if change_type == ChangeType.SPELLING:
            return f"Spelling correction"
        elif change_type == ChangeType.GRAMMAR:
            return f"Grammar improvement"
        else:
            return f"Text improvement"
