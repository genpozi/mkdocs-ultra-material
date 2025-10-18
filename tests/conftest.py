"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
from mkdocs_ai.cache import CacheManager


@pytest.fixture
def temp_cache_dir(tmp_path):
    """Provide a temporary cache directory."""
    cache_dir = tmp_path / ".ai-cache"
    cache_dir.mkdir()
    return cache_dir


@pytest.fixture
def cache_manager(temp_cache_dir):
    """Provide a CacheManager instance with temporary directory."""
    return CacheManager(
        cache_dir=str(temp_cache_dir),
        ttl=3600,
        max_size=1024 * 1024,  # 1MB
    )


@pytest.fixture
def sample_prompt():
    """Provide a sample prompt for testing."""
    return "Create a guide about Docker networking"


@pytest.fixture
def sample_response():
    """Provide a sample AI response for testing."""
    return "# Docker Networking Guide\n\nDocker provides several networking options..."


@pytest.fixture
def mock_provider_config():
    """Provide mock provider configuration."""
    return {
        "name": "openrouter",
        "api_key": "test-key",
        "model": "test-model",
        "temperature": 0.7,
        "max_tokens": 4000,
    }
