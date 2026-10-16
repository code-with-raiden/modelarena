"""
ModelArena — Provider Registry
OpenRouter is now the primary provider — one key, all models.
"""
from .base import BaseProvider, ProviderResponse
from .anthropic import AnthropicProvider
from .openai import OpenAIProvider
from .groq import GroqProvider
from .google import GoogleProvider
from .openrouter import OpenRouterProvider

# model_id → (ProviderClass, api_key_name)
MODEL_REGISTRY: dict[str, tuple[type[BaseProvider], str]] = {

    # ── Via OpenRouter (your workspace key covers all of these) ──────
    "anthropic/claude-3-haiku":          (OpenRouterProvider, "openrouter"),
    "anthropic/claude-3.5-sonnet":       (OpenRouterProvider, "openrouter"),
    "openai/gpt-4o-mini":                (OpenRouterProvider, "openrouter"),
    "openai/gpt-4o":                     (OpenRouterProvider, "openrouter"),
    "meta-llama/llama-3.3-70b-instruct": (OpenRouterProvider, "openrouter"),
    "mistralai/mistral-large":           (OpenRouterProvider, "openrouter"),
    "google/gemini-2.0-flash-001":       (OpenRouterProvider, "openrouter"),
    "deepseek/deepseek-chat":            (OpenRouterProvider, "openrouter"),
    "qwen/qwen-2.5-72b-instruct":        (OpenRouterProvider, "openrouter"),
    "microsoft/phi-4":                   (OpenRouterProvider, "openrouter"),

    # ── Direct provider keys (optional fallback) ─────────────────────
    "claude-haiku-5-5":                  (AnthropicProvider,  "anthropic"),
    "gpt-4o-mini":                       (OpenAIProvider,     "openai"),
    "llama-3.3-70b-versatile":           (GroqProvider,       "groq"),
    "gemini-2.0-flash":                  (GoogleProvider,     "google"),
}


def get_provider(model_id: str, api_keys: dict[str, str]) -> BaseProvider:
    if model_id not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: {model_id}")
    cls, key_name = MODEL_REGISTRY[model_id]
    api_key = api_keys.get(key_name, "")
    return cls(api_key=api_key, model_id=model_id)


def list_models() -> list[dict]:
    return [
        {
            "id": mid,
            "provider": cls.provider_name,
            "key_required": key,
            "via_openrouter": key == "openrouter",
        }
        for mid, (cls, key) in MODEL_REGISTRY.items()
    ]
