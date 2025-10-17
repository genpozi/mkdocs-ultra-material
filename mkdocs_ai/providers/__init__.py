"""AI provider abstraction layer."""

from .base import AIProvider, ProviderError, ProviderResponse
from .openrouter import OpenRouterProvider
from .gemini import GeminiProvider
from .anthropic import AnthropicProvider
from .ollama import OllamaProvider

__all__ = [
    "AIProvider",
    "ProviderError",
    "ProviderResponse",
    "OpenRouterProvider",
    "GeminiProvider",
    "AnthropicProvider",
    "OllamaProvider",
    "get_provider",
]


def get_provider(config: dict) -> AIProvider:
    """Factory function to get the appropriate provider."""
    provider_name = config.get("name", "openrouter")
    
    providers = {
        "openrouter": OpenRouterProvider,
        "gemini": GeminiProvider,
        "anthropic": AnthropicProvider,
        "ollama": OllamaProvider,
    }
    
    provider_class = providers.get(provider_name)
    if not provider_class:
        raise ValueError(f"Unknown provider: {provider_name}")
    
    return provider_class(config)
