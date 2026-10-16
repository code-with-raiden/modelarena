"""
ModelArena — Provider Registry
Add a new model by adding one entry to MODEL_REGISTRY.
"""
from .base import BaseProvider, ProviderResponse
from .anthropic import AnthropicProvider
from .openai import OpenAIProvider
from .groq import GroqProvider
from .google import GoogleProvider

# model_id → (ProviderClass, api_key_name)
MODEL_REGISTRY: dict[str, tuple[type[BaseProvider], str]] = {
    # Anthropic
    "claude-haiku-5-5":    (AnthropicProvider, "anthropic"),
    "claude-sonnet-4-6":   (AnthropicProvider, "anthropic"),
    # OpenAI
    "gpt-4o-mini":         (OpenAIProvider,    "openai"),
    "gpt-4o":              (OpenAIProvider,    "openai"),
    # Groq (Llama, Mixtral)
    "llama-3.3-70b-versatile": (GroqProvider,  "groq"),
    "mixtral-8x7b-32768":      (GroqProvider,  "groq"),
    # Google
    "gemini-2.0-flash":    (GoogleProvider,    "google"),
    "gemini-1.5-pro":      (GoogleProvider,    "google"),
}


def get_provider(model_id: str, api_keys: dict[str, str]) -> BaseProvider:
    if model_id not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: {model_id}")
    cls, key_name = MODEL_REGISTRY[model_id]
    api_key = api_keys.get(key_name, "")
    return cls(api_key=api_key, model_id=model_id)


def list_models() -> list[dict]:
    return [
        {"id": mid, "provider": cls.provider_name, "key_required": key}
        for mid, (cls, key) in MODEL_REGISTRY.items()
    ]
