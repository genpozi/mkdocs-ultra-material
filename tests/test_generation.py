"""Tests for document generation."""

import pytest
from mkdocs_ai.generation.prompt import PromptGenerator
from mkdocs_ai.generation.markdown import MarkdownProcessor


def test_prompt_generator_init():
    """Test prompt generator initialization."""
    generator = PromptGenerator()
    assert generator is not None


def test_prompt_generator_build_prompt():
    """Test building a generation prompt."""
    generator = PromptGenerator()
    prompt = generator.build_prompt(
        user_prompt="Create a Docker guide",
        context={"topic": "networking"},
    )
    
    assert "Docker guide" in prompt
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_markdown_processor_init():
    """Test markdown processor initialization."""
    processor = MarkdownProcessor()
    assert processor is not None


def test_markdown_processor_find_ai_comments():
    """Test finding AI-GENERATE comments."""
    processor = MarkdownProcessor()
    content = """
# Title

<!-- AI-GENERATE: Create a section about Docker -->

## Another Section
"""
    
    comments = processor.find_ai_comments(content)
    assert len(comments) > 0
    assert "Docker" in comments[0]["prompt"]


def test_markdown_processor_find_ai_blocks():
    """Test finding AI-GENERATE blocks."""
    processor = MarkdownProcessor()
    content = """
# Title

<!-- AI-GENERATE-START: docker-guide -->
Create a comprehensive Docker guide
<!-- AI-GENERATE-END -->
"""
    
    blocks = processor.find_ai_blocks(content)
    assert len(blocks) > 0
    assert "docker-guide" in blocks[0]["id"]


def test_markdown_processor_no_comments():
    """Test markdown without AI comments."""
    processor = MarkdownProcessor()
    content = """
# Title

Regular content without AI comments.
"""
    
    comments = processor.find_ai_comments(content)
    blocks = processor.find_ai_blocks(content)
    
    assert len(comments) == 0
    assert len(blocks) == 0


def test_prompt_generator_with_template():
    """Test prompt generation with template context."""
    generator = PromptGenerator()
    
    context = {
        "service_name": "Plex",
        "port": 32400,
        "features": ["streaming", "remote access"],
    }
    
    prompt = generator.build_prompt(
        user_prompt="Document this service",
        context=context,
    )
    
    assert "Plex" in prompt or "service" in prompt.lower()
