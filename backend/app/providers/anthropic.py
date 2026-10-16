"""
ModelArena — Anthropic Provider (Claude models)
"""
import time
import anthropic
from .base import BaseProvider, ProviderResponse


class AnthropicProvider(BaseProvider):
    provider_name = "Anthropic"

    async def complete(self, prompt: str, system: str = "") -> ProviderResponse:
        client = anthropic.AsyncAnthropic(api_key=self.api_key)
        start = time.monotonic()
        try:
            msg = await client.messages.create(
                model=self.model_id,
                max_tokens=1024,
                system=system or "You are a helpful assistant.",
                messages=[{"role": "user", "content": prompt}],
            )
            latency = int((time.monotonic() - start) * 1000)
            return ProviderResponse(
                model_id=self.model_id,
                content=msg.content[0].text,
                latency_ms=latency,
                tokens_used=msg.usage.input_tokens + msg.usage.output_tokens,
            )
        except Exception as e:
            return ProviderResponse(
                model_id=self.model_id, content="",
                latency_ms=0, error=str(e)
            )
