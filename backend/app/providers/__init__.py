"""
ModelArena — Provider Registry
Primary: OpenRouter (one key, 100+ models, uses your workspace credits)
Fallback: direct provider keys
"""
from .base import BaseProvider, ProviderResponse
from .anthropic import AnthropicProvider
from .openai import OpenAIProvider
from .groq import GroqProvider
from .google import GoogleProvider
from .mistral import MistralProvider
from .together import TogetherProvider
from .openrouter import OpenRouterProvider

# model_id → (ProviderClass, api_key_name)
MODEL_REGISTRY: dict[str, tuple[type[BaseProvider], str]] = {

    # ── OpenRouter — recommended (workspace credits work here) ───────
    "anthropic/claude-3-haiku":           (OpenRouterProvider, "openrouter"),
    "anthropic/claude-3.5-sonnet":        (OpenRouterProvider, "openrouter"),
    "anthropic/claude-3-opus":            (OpenRouterProvider, "openrouter"),
    "openai/gpt-4o-mini":                 (OpenRouterProvider, "openrouter"),
    "openai/gpt-4o":                      (OpenRouterProvider, "openrouter"),
    "meta-llama/llama-3.3-70b-instruct":  (OpenRouterProvider, "openrouter"),
    "meta-llama/llama-3.1-8b-instruct":   (OpenRouterProvider, "openrouter"),
    "mistralai/mistral-large":            (OpenRouterProvider, "openrouter"),
    "mistralai/mixtral-8x7b-instruct":    (OpenRouterProvider, "openrouter"),
    "google/gemini-2.0-flash-001":        (OpenRouterProvider, "openrouter"),
    "google/gemini-flash-1.5":            (OpenRouterProvider, "openrouter"),
    "deepseek/deepseek-chat":             (OpenRouterProvider, "openrouter"),
    "deepseek/deepseek-r1":               (OpenRouterProvider, "openrouter"),
    "qwen/qwen-2.5-72b-instruct":         (OpenRouterProvider, "openrouter"),
    "microsoft/phi-4":                    (OpenRouterProvider, "openrouter"),
    "cohere/command-r-plus":              (OpenRouterProvider, "openrouter"),

    # ── Direct provider keys (optional) ─────────────────────────────
    "claude-haiku-direct":    (AnthropicProvider, "anthropic"),
    "gpt-4o-mini-direct":     (OpenAIProvider,    "openai"),
    "llama-3.3-70b-direct":   (GroqProvider,      "groq"),
    "gemini-flash-direct":    (GoogleProvider,     "google"),
    "mistral-large-direct":   (MistralProvider,   "mistral"),
    "qwen-2.5-direct":        (TogetherProvider,  "together"),
}

# Default set for quick evaluations
DEFAULT_MODELS = [
    "anthropic/claude-3-haiku",
    "openai/gpt-4o-mini",
    "meta-llama/llama-3.3-70b-instruct",
    "google/gemini-2.0-flash-001",
    "deepseek/deepseek-chat",
]


def get_provider(model_id: str, api_keys: dict[str, str]) -> BaseProvider:
    if model_id not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: '{model_id}'. Call GET /models to see available models.")
    cls, key_name = MODEL_REGISTRY[model_id]
    api_key = api_keys.get(key_name, "")
    return cls(api_key=api_key, model_id=model_id)


def list_models() -> list[dict]:
    return [
        {
            "id": mid,
            "provider": cls.provider_name,
            "key_required": key,
            "recommended": key == "openrouter",
        }
        for mid, (cls, key) in MODEL_REGISTRY.items()
    ]
