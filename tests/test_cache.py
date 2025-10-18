"""Tests for cache manager."""

import pytest
from mkdocs_ai.cache import CacheManager


def test_cache_manager_init(temp_cache_dir):
    """Test cache manager initialization."""
    cache = CacheManager(
        cache_dir=str(temp_cache_dir),
        ttl=3600,
        max_size=1024 * 1024,
    )
    assert cache.cache_dir == temp_cache_dir
    assert cache.ttl == 3600


def test_cache_set_and_get(cache_manager, sample_prompt, sample_response):
    """Test setting and getting cache values."""
    # Set value
    cache_manager.set(sample_prompt, sample_response, model="test")
    
    # Get value
    result = cache_manager.get(sample_prompt, model="test")
    assert result == sample_response


def test_cache_miss(cache_manager):
    """Test cache miss returns None."""
    result = cache_manager.get("nonexistent-key")
    assert result is None


def test_cache_clear(cache_manager, sample_prompt, sample_response):
    """Test cache clearing."""
    # Set value
    cache_manager.set(sample_prompt, sample_response, model="test")
    assert cache_manager.get(sample_prompt, model="test") is not None
    
    # Clear cache
    cache_manager.clear()
    assert cache_manager.get(sample_prompt, model="test") is None


def test_cache_stats(cache_manager, sample_prompt, sample_response):
    """Test cache statistics."""
    cache_manager.set(sample_prompt, sample_response, model="test")
    
    stats = cache_manager.get_stats()
    assert "size" in stats
    assert "count" in stats
    assert stats["count"] >= 1


def test_cache_key_generation(cache_manager):
    """Test cache key generation is deterministic."""
    prompt = "test prompt"
    params = {"model": "test", "temperature": 0.7}
    
    key1 = cache_manager._generate_key(prompt, params)
    key2 = cache_manager._generate_key(prompt, params)
    
    assert key1 == key2


def test_cache_key_different_params(cache_manager):
    """Test different parameters generate different keys."""
    prompt = "test prompt"
    
    key1 = cache_manager._generate_key(prompt, {"model": "model1"})
    key2 = cache_manager._generate_key(prompt, {"model": "model2"})
    
    assert key1 != key2
