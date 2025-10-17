"""Data models for content enhancement."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ChangeType(Enum):
    """Type of enhancement change."""
    
    GRAMMAR = "grammar"
    SPELLING = "spelling"
    CLARITY = "clarity"
    CONSISTENCY = "consistency"
    SEO = "seo"
    LINK = "link"


@dataclass
class Change:
    """Represents a single enhancement change."""
    
    type: ChangeType
    line_number: Optional[int]
    original: str
    enhanced: str
    reason: str
    confidence: float = 1.0
    
    def __str__(self) -> str:
        """String representation of change."""
        location = f"Line {self.line_number}: " if self.line_number else ""
        return f"{location}{self.original!r} → {self.enhanced!r} ({self.reason})"


@dataclass
class EnhancementOptions:
    """Options for content enhancement."""
    
    grammar: bool = True
    clarity: bool = True
    consistency: bool = True
    seo: bool = False
    links: bool = False
    
    # Preservation options
    preserve_code: bool = True
    preserve_frontmatter: bool = True
    preserve_html: bool = True
    preserve_tables: bool = True
    preserve_math: bool = True
    
    # AI options
    temperature: float = 0.3
    max_tokens: int = 4000
    
    # Glossary for consistency
    glossary: dict[str, str] = field(default_factory=dict)


@dataclass
class EnhancementResult:
    """Result of content enhancement."""
    
    original: str
    enhanced: str
    diff: str
    changes: list[Change]
    
    @property
    def has_changes(self) -> bool:
        """Check if any changes were made."""
        return len(self.changes) > 0
    
    @property
    def change_count(self) -> int:
        """Total number of changes."""
        return len(self.changes)
    
    def changes_by_type(self, change_type: ChangeType) -> list[Change]:
        """Get changes of a specific type."""
        return [c for c in self.changes if c.type == change_type]
    
    def summary(self) -> str:
        """Generate summary of changes."""
        if not self.has_changes:
            return "No changes made."
        
        summary_lines = [f"Total changes: {self.change_count}"]
        
        for change_type in ChangeType:
            type_changes = self.changes_by_type(change_type)
            if type_changes:
                summary_lines.append(
                    f"  {change_type.value.capitalize()}: {len(type_changes)}"
                )
        
        return "\n".join(summary_lines)


@dataclass
class Placeholder:
    """Represents a placeholder for protected content."""
    
    id: str
    content: str
    type: str  # 'code_block', 'inline_code', 'frontmatter', etc.
    
    def __str__(self) -> str:
        """String representation (the placeholder itself)."""
        return f"__PLACEHOLDER_{self.type.upper()}_{self.id}__"


@dataclass
class EnhancementConfig:
    """Configuration for enhancement system."""
    
    enabled: bool = True
    auto_enhance: bool = False
    
    # Features
    features: list[str] = field(default_factory=lambda: [
        "grammar", "clarity", "consistency"
    ])
    
    # Provider settings
    provider: str = "openrouter"
    model: str = "anthropic/claude-3.5-sonnet"
    temperature: float = 0.3
    
    # Glossary
    glossary: dict[str, str] = field(default_factory=dict)
    
    # Exclusions
    exclude: list[str] = field(default_factory=list)
    
    def should_enhance(self, file_path: str) -> bool:
        """Check if file should be enhanced."""
        if not self.enabled:
            return False
        
        # Check exclusions
        for pattern in self.exclude:
            if pattern in file_path:
                return False
        
        return True
    
    def get_options(self) -> EnhancementOptions:
        """Get enhancement options from config."""
        return EnhancementOptions(
            grammar="grammar" in self.features,
            clarity="clarity" in self.features,
            consistency="consistency" in self.features,
            seo="seo" in self.features,
            links="links" in self.features,
            temperature=self.temperature,
            glossary=self.glossary
        )
