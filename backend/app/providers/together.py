"""
ModelArena — Together AI Provider (Qwen, DBRX, etc.)
OpenAI-compatible endpoint.
"""
import time
from openai import AsyncOpenAI
from .base import BaseProvider, ProviderResponse

TOGETHER_BASE = "https://api.together.xyz/v1"


class TogetherProvider(BaseProvider):
    provider_name = "Together AI"

    async def complete(self, prompt: str, system: str = "") -> ProviderResponse:
        client = AsyncOpenAI(api_key=self.api_key, base_url=TOGETHER_BASE)
        start = time.monotonic()
        try:
            res = await client.chat.completions.create(
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
