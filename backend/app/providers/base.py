"""
ModelArena — Abstract BaseProvider
Every AI provider implements this interface.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ProviderResponse:
    model_id: str
    content: str
    latency_ms: int
    tokens_used: int = 0
    error: str | None = None


class BaseProvider(ABC):
    def __init__(self, api_key: str, model_id: str):
        self.api_key = api_key
        self.model_id = model_id

    @abstractmethod
    async def complete(self, prompt: str, system: str = "") -> ProviderResponse:
        """Send prompt, return ProviderResponse."""
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        ...
