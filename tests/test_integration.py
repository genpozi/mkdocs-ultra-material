"""Integration tests for MkDocs Ultra Material."""

import pytest
from pathlib import Path
from mkdocs_ai.config import AIAssistantConfig
from mkdocs_ai.providers import get_provider
from mkdocs_ai.cache import CacheManager


def test_config_initialization():
    """Test that configuration initializes with defaults."""
    config = AIAssistantConfig()
    
    assert config.enabled is True
    assert config.provider.name == "openrouter"
    assert config.cache.enabled is True
    assert config.generation.enabled is True


def test_provider_factory():
    """Test provider factory creates correct providers."""
    configs = [
        {"name": "openrouter", "api_key": "test", "model": "test-model"},
        {"name": "gemini", "api_key": "test", "model": "gemini-pro"},
        {"name": "anthropic", "api_key": "test", "model": "claude-3-5-sonnet-20241022"},
        {"name": "ollama", "base_url": "http://localhost:11434", "model": "llama2"},
    ]
    
    for config in configs:
        provider = get_provider(config)
        assert provider is not None
        assert provider.name == config["name"]


def test_cache_workflow(tmp_path):
    """Test complete cache workflow."""
    cache_dir = tmp_path / ".ai-cache"
    cache = CacheManager(str(cache_dir), ttl=3600)
    
    # Set and get
    prompt = "Test prompt"
    response = "Test response"
    cache.set(prompt, response, model="test-model")
    
    result = cache.get(prompt, model="test-model")
    assert result == response
    
    # Stats
    stats = cache.get_stats()
    assert stats["count"] >= 1
    
    # Clear
    cache.clear()
    result = cache.get(prompt, model="test-model")
    assert result is None
    
    cache.close()


def test_module_imports():
    """Test that all modules can be imported."""
    # Core modules
    from mkdocs_ai import AIAssistantPlugin, __version__
    assert AIAssistantPlugin is not None
    assert __version__ == "0.5.0"
    
    # Providers
    from mkdocs_ai.providers import (
        AIProvider,
        ProviderError,
        ProviderResponse,
        OpenRouterProvider,
        GeminiProvider,
        AnthropicProvider,
        OllamaProvider,
    )
    
    # Generation
    from mkdocs_ai.generation import PromptGenerator, MarkdownProcessor
    
    # Enhancement
    from mkdocs_ai.enhancement import (
        EnhancementPipeline,
        EnhancementOptions,
        GrammarEnhancer,
        ClarityEnhancer,
        ConsistencyChecker,
    )
    
    # Search
    from mkdocs_ai.search import (
        PageChunk,
        SearchResult,
        EmbeddingGenerator,
        VectorIndex,
    )
    
    # Assets
    from mkdocs_ai.assets import (
        AssetProcessor,
        AssetDiscovery,
        Asset,
        AssetProcessorOrchestrator,
    )
    
    # Obelisk
    from mkdocs_ai.obelisk import (
        ObeliskClient,
        DocumentationExporter,
        DocumentationAnalytics,
        ObeliskDocument,
    )


def test_plugin_initialization():
    """Test plugin can be initialized."""
    from mkdocs_ai.plugin import AIAssistantPlugin
    
    plugin = AIAssistantPlugin()
    assert plugin is not None
    assert plugin.provider is None  # Not initialized yet
    assert plugin.cache_manager is None


def test_generation_prompt_builder():
    """Test prompt generator can be created."""
    from mkdocs_ai.generation import PromptGenerator
    from mkdocs_ai.providers import get_provider
    
    provider = get_provider({
        "name": "openrouter",
        "api_key": "test",
        "model": "test-model",
    })
    
    generator = PromptGenerator(provider)
    assert generator is not None
    assert generator.provider == provider


def test_markdown_processor_patterns():
    """Test markdown processor can detect AI comments."""
    from mkdocs_ai.generation import MarkdownProcessor
    from mkdocs_ai.providers import get_provider
    
    provider = get_provider({
        "name": "openrouter",
        "api_key": "test",
        "model": "test-model",
    })
    
    processor = MarkdownProcessor(provider)
    
    # Test simple comment detection
    markdown_with_comment = "# Title\n\n<!-- AI-GENERATE: test -->\n\nContent"
    assert processor.has_ai_comments(markdown_with_comment)
    
    # Test no comments
    markdown_without = "# Title\n\nContent"
    assert not processor.has_ai_comments(markdown_without)


def test_search_index_creation():
    """Test search index can be created and used."""
    from mkdocs_ai.search import VectorIndex, PageChunk
    
    index = VectorIndex()
    assert index is not None
    assert len(index.chunks) == 0
    
    # Add test chunks
    chunks = [
        PageChunk(
            page_url="/test",
            title="Test Page",
            text="Test content",
            embedding=[0.1, 0.2, 0.3],
            start_pos=0,
            end_pos=12,
        )
    ]
    
    index.add_chunks(chunks)
    assert len(index.chunks) == 1


def test_asset_discovery():
    """Test asset discovery can find files."""
    from mkdocs_ai.assets import AssetDiscovery
    
    discovery = AssetDiscovery()
    assert discovery is not None
    
    # Test Python file discovery
    python_files = discovery.discover_python_modules(Path("mkdocs_ai"))
    assert len(python_files) > 0
    assert all(f.suffix == ".py" for f in python_files)


def test_obelisk_models():
    """Test Obelisk models can be created."""
    from mkdocs_ai.obelisk import ObeliskDocument, ObeliskQuery
    
    doc = ObeliskDocument(
        id="test-doc",
        title="Test Document",
        content="Test content",
        url="https://example.com/test",
        metadata={"source": "test"},
    )
    
    assert doc.id == "test-doc"
    assert doc.title == "Test Document"
    
    query = ObeliskQuery(
        question="What is this?",
        max_results=5,
    )
    
    assert query.question == "What is this?"
    assert query.max_results == 5


@pytest.mark.asyncio
async def test_provider_validation():
    """Test provider validation works."""
    from mkdocs_ai.providers import get_provider, ProviderError
    
    # Valid config
    provider = get_provider({
        "name": "openrouter",
        "api_key": "test-key",
        "model": "test-model",
    })
    
    # Should not raise
    provider.validate_config()
    
    # Missing API key
    provider_no_key = get_provider({
        "name": "openrouter",
        "model": "test-model",
    })
    
    with pytest.raises(ProviderError):
        provider_no_key.validate_config()
