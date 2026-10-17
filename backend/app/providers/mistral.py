"""
ModelArena — Mistral AI Provider
"""
import time
from mistralai import AsyncMistral
from .base import BaseProvider, ProviderResponse


class MistralProvider(BaseProvider):
    provider_name = "Mistral"

    async def complete(self, prompt: str, system: str = "") -> ProviderResponse:
        client = AsyncMistral(api_key=self.api_key)
        start = time.monotonic()
        try:
            res = await client.chat.complete_async(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": system or "You are a helpful assistant."},
                    {"role": "user",   "content": prompt},
                ],
                max_tokens=1024,
            )
            latency = int((time.monotonic() - start) * 1000)
            return ProviderResponse(
                model_id=self.model_id,
                content=res.choices[0].message.content,
                latency_ms=latency,
                tokens_used=res.usage.total_tokens if res.usage else 0,
            )
        except Exception as e:
            return ProviderResponse(
                model_id=self.model_id, content="",
                latency_ms=0, error=str(e)
            )
