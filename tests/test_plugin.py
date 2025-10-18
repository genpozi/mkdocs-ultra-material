"""Tests for MkDocs plugin."""

import pytest
from mkdocs_ai.plugin import AIAssistantPlugin
from mkdocs_ai.config import AIAssistantConfig


def test_plugin_init():
    """Test plugin initialization."""
    plugin = AIAssistantPlugin()
    assert plugin is not None
    assert plugin.provider is None
    assert plugin.cache_manager is None


def test_plugin_config():
    """Test plugin configuration."""
    plugin = AIAssistantPlugin()
    config = AIAssistantConfig()
    
    assert config.enabled is True
    assert config.provider.name == "openrouter"


def test_plugin_startup():
    """Test plugin startup hook."""
    plugin = AIAssistantPlugin()
    plugin.config = AIAssistantConfig()
    
    # Should not raise
    plugin.on_startup(command="build", dirty=False)
    assert plugin.is_serve is False
    
    plugin.on_startup(command="serve", dirty=False)
    assert plugin.is_serve is True


def test_plugin_disabled():
    """Test plugin when disabled."""
    plugin = AIAssistantPlugin()
    config = AIAssistantConfig()
    config.enabled = False
    plugin.config = config
    
    # Should handle gracefully
    plugin.on_startup(command="build", dirty=False)
