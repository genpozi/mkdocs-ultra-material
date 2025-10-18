"""Tests for configuration."""

import pytest
from mkdocs_ai.config import AIAssistantConfig


def test_config_defaults():
    """Test configuration default values."""
    config = AIAssistantConfig()
    
    assert config.enabled is True
    assert config.debug is False
    assert config.provider.name == "openrouter"
    assert config.cache.enabled is True
    assert config.cache.ttl == 86400


def test_config_provider_settings():
    """Test provider configuration."""
    config = AIAssistantConfig()
    
    assert config.provider.temperature == 0.7
    assert config.provider.max_tokens == 4000
    assert config.provider.timeout == 30


def test_config_cache_settings():
    """Test cache configuration."""
    config = AIAssistantConfig()
    
    assert config.cache.dir == ".ai-cache"
    assert config.cache.max_size == 1073741824  # 1GB


def test_config_generation_settings():
    """Test generation configuration."""
    config = AIAssistantConfig()
    
    assert config.generation.enabled is True
    assert config.generation.output_dir == "docs/generated"
    assert config.generation.cli_enabled is True
    assert config.generation.markdown_syntax is True


def test_config_enhancement_settings():
    """Test enhancement configuration."""
    config = AIAssistantConfig()
    
    assert config.enhancement.enabled is False
    assert config.enhancement.auto_enhance is False
    assert config.enhancement.preserve_code is True


def test_config_search_settings():
    """Test search configuration."""
    config = AIAssistantConfig()
    
    assert config.search.enabled is False
    assert config.search.chunk_size == 1000
    assert config.search.chunk_overlap == 200


def test_config_assets_settings():
    """Test assets configuration."""
    config = AIAssistantConfig()
    
    assert config.assets.enabled is False
    assert config.assets.auto_discover is True


def test_config_obelisk_settings():
    """Test obelisk configuration."""
    config = AIAssistantConfig()
    
    assert config.obelisk.enabled is False
