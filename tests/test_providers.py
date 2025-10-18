"""Tests for AI providers."""

import pytest
from mkdocs_ai.providers import get_provider, ProviderError
from mkdocs_ai.providers.base import AIProvider


def test_get_provider_openrouter(mock_provider_config):
    """Test getting OpenRouter provider."""
    provider = get_provider(mock_provider_config)
    assert provider is not None
    assert provider.name == "openrouter"


def test_get_provider_gemini():
    """Test getting Gemini provider."""
    config = {
        "name": "gemini",
        "api_key": "test-key",
        "model": "gemini-pro",
    }
    provider = get_provider(config)
    assert provider is not None
    assert provider.name == "gemini"


def test_get_provider_anthropic():
    """Test getting Anthropic provider."""
    config = {
        "name": "anthropic",
        "api_key": "test-key",
        "model": "claude-3-5-sonnet-20241022",
    }
    provider = get_provider(config)
    assert provider is not None
    assert provider.name == "anthropic"


def test_get_provider_ollama():
    """Test getting Ollama provider."""
    config = {
        "name": "ollama",
        "base_url": "http://localhost:11434",
        "model": "llama2",
    }
    provider = get_provider(config)
    assert provider is not None
    assert provider.name == "ollama"


def test_get_provider_invalid():
    """Test getting invalid provider raises error."""
    config = {
        "name": "invalid-provider",
        "api_key": "test-key",
    }
    with pytest.raises(ProviderError):
        get_provider(config)


def test_provider_validate_config_missing_api_key():
    """Test provider validation fails without API key."""
    config = {
        "name": "openrouter",
        "model": "test-model",
    }
    provider = get_provider(config)
    
    with pytest.raises(ProviderError, match="API key"):
        provider.validate_config()


def test_provider_validate_config_missing_model():
    """Test provider validation fails without model."""
    config = {
        "name": "openrouter",
        "api_key": "test-key",
    }
    provider = get_provider(config)
    
    with pytest.raises(ProviderError, match="model"):
        provider.validate_config()


def test_provider_config_defaults(mock_provider_config):
    """Test provider uses default values."""
    provider = get_provider(mock_provider_config)
    
    assert provider.temperature == 0.7
    assert provider.max_tokens == 4000
    assert provider.timeout == 30
