"""
ModelArena — OpenRouter Provider
Single API key → 100+ models (Claude, GPT-4, Llama, Mistral, Gemini...)
Docs: https://openrouter.ai/docs
"""
import time
from openai import AsyncOpenAI
from .base import BaseProvider, ProviderResponse

OPENROUTER_BASE = "https://openrouter.ai/api/v1"


class OpenRouterProvider(BaseProvider):
    provider_name = "OpenRouter"

    async def complete(self, prompt: str, system: str = "") -> ProviderResponse:
        client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=OPENROUTER_BASE,
        )
        start = time.monotonic()
        try:
            res = await client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": system or "You are a helpful assistant."},
                    {"role": "user",   "content": prompt},
                ],
                max_tokens=1024,
                extra_headers={
                    "HTTP-Referer": "https://github.com/code-with-raiden/modelarena",
                    "X-Title": "ModelArena",
                },
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
