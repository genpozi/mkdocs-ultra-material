"""Content preservation for enhancement."""

import re
import uuid
from typing import Optional

from .models import Placeholder


class ContentPreserver:
    """Preserves technical content during enhancement.
    
    Extracts and replaces protected content (code blocks, frontmatter, etc.)
    with placeholders, then restores them after enhancement.
    """
    
    def __init__(self):
        """Initialize content preserver."""
        self.placeholders: dict[str, Placeholder] = {}
        self._counter = 0
    
    def extract(self, markdown: str) -> str:
        """Extract protected content, return prose with placeholders.
        
        Args:
            markdown: Original markdown content
            
        Returns:
            Markdown with protected content replaced by placeholders
        """
        # Extract in order (most specific to least specific)
        markdown = self._extract_frontmatter(markdown)
        markdown = self._extract_fenced_code_blocks(markdown)
        markdown = self._extract_indented_code_blocks(markdown)
        markdown = self._extract_html_blocks(markdown)
        markdown = self._extract_math_blocks(markdown)
        markdown = self._extract_tables(markdown)
        markdown = self._extract_inline_code(markdown)
        markdown = self._extract_html_tags(markdown)
        
        return markdown
    
    def restore(self, markdown: str) -> str:
        """Restore protected content from placeholders.
        
        Args:
            markdown: Markdown with placeholders
            
        Returns:
            Markdown with original content restored
        """
        result = markdown
        
        # Restore in reverse order
        for placeholder_id, placeholder in self.placeholders.items():
            placeholder_str = str(placeholder)
            result = result.replace(placeholder_str, placeholder.content)
        
        return result
    
    def clear(self):
        """Clear all placeholders."""
        self.placeholders.clear()
        self._counter = 0
    
    def _create_placeholder(self, content: str, content_type: str) -> str:
        """Create a placeholder for protected content.
        
        Args:
            content: Content to protect
            content_type: Type of content (e.g., 'code_block', 'frontmatter')
            
        Returns:
            Placeholder string
        """
        placeholder_id = f"{self._counter:04d}"
        self._counter += 1
        
        placeholder = Placeholder(
            id=placeholder_id,
            content=content,
            type=content_type
        )
        
        self.placeholders[placeholder_id] = placeholder
        return str(placeholder)
    
    def _extract_frontmatter(self, markdown: str) -> str:
        """Extract YAML/TOML frontmatter.
        
        Patterns:
        - YAML: ---\n...\n---
        - TOML: +++\n...\n+++
        """
        # YAML frontmatter
        yaml_pattern = r'^---\n(.*?)\n---\n'
        match = re.match(yaml_pattern, markdown, re.DOTALL)
        if match:
            frontmatter = match.group(0)
            placeholder = self._create_placeholder(frontmatter, 'frontmatter')
            markdown = markdown.replace(frontmatter, placeholder, 1)
        
        # TOML frontmatter
        toml_pattern = r'^\+\+\+\n(.*?)\n\+\+\+\n'
        match = re.match(toml_pattern, markdown, re.DOTALL)
        if match:
            frontmatter = match.group(0)
            placeholder = self._create_placeholder(frontmatter, 'frontmatter')
            markdown = markdown.replace(frontmatter, placeholder, 1)
        
        return markdown
    
    def _extract_fenced_code_blocks(self, markdown: str) -> str:
        """Extract fenced code blocks (```...```)."""
        pattern = r'```[\s\S]*?```'
        
        def replace_code_block(match):
            code_block = match.group(0)
            return self._create_placeholder(code_block, 'code_block')
        
        return re.sub(pattern, replace_code_block, markdown)
    
    def _extract_indented_code_blocks(self, markdown: str) -> str:
        """Extract indented code blocks (4 spaces or tab)."""
        # Match lines that start with 4 spaces or a tab
        pattern = r'(?:^|\n)((?:(?:    |\t).*\n)+)'
        
        def replace_code_block(match):
            code_block = match.group(1)
            return '\n' + self._create_placeholder(code_block, 'code_block')
        
        return re.sub(pattern, replace_code_block, markdown)
    
    def _extract_inline_code(self, markdown: str) -> str:
        """Extract inline code (`...`)."""
        pattern = r'`[^`\n]+`'
        
        def replace_inline_code(match):
            inline_code = match.group(0)
            return self._create_placeholder(inline_code, 'inline_code')
        
        return re.sub(pattern, replace_inline_code, markdown)
    
    def _extract_html_blocks(self, markdown: str) -> str:
        """Extract HTML blocks."""
        # Match HTML blocks (tags on their own lines)
        pattern = r'(?:^|\n)(<[a-zA-Z][^>]*>[\s\S]*?</[a-zA-Z][^>]*>)(?:\n|$)'
        
        def replace_html_block(match):
            html_block = match.group(1)
            return '\n' + self._create_placeholder(html_block, 'html_block') + '\n'
        
        return re.sub(pattern, replace_html_block, markdown)
    
    def _extract_html_tags(self, markdown: str) -> str:
        """Extract inline HTML tags."""
        pattern = r'<[a-zA-Z][^>]*>.*?</[a-zA-Z][^>]*>'
        
        def replace_html_tag(match):
            html_tag = match.group(0)
            return self._create_placeholder(html_tag, 'html_tag')
        
        return re.sub(pattern, replace_html_tag, markdown)
    
    def _extract_math_blocks(self, markdown: str) -> str:
        """Extract LaTeX math blocks ($$...$$)."""
        # Block math
        pattern = r'\$\$[\s\S]*?\$\$'
        
        def replace_math_block(match):
            math_block = match.group(0)
            return self._create_placeholder(math_block, 'math_block')
        
        markdown = re.sub(pattern, replace_math_block, markdown)
        
        # Inline math
        pattern = r'\$[^\$\n]+\$'
        
        def replace_inline_math(match):
            inline_math = match.group(0)
            return self._create_placeholder(inline_math, 'inline_math')
        
        return re.sub(pattern, replace_inline_math, markdown)
    
    def _extract_tables(self, markdown: str) -> str:
        """Extract markdown tables."""
        # Match tables (lines with | separators)
        pattern = r'(?:^|\n)(\|.+\|(?:\n\|.+\|)+)(?:\n|$)'
        
        def replace_table(match):
            table = match.group(1)
            return '\n' + self._create_placeholder(table, 'table') + '\n'
        
        return re.sub(pattern, replace_table, markdown)
    
    def get_stats(self) -> dict[str, int]:
        """Get statistics about preserved content.
        
        Returns:
            Dictionary with counts by content type
        """
        stats: dict[str, int] = {}
        
        for placeholder in self.placeholders.values():
            content_type = placeholder.type
            stats[content_type] = stats.get(content_type, 0) + 1
        
        return stats
