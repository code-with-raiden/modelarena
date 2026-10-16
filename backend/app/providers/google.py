"""
ModelArena — Google AI Provider (Gemini models)
"""
import time
import google.generativeai as genai
from .base import BaseProvider, ProviderResponse


class GoogleProvider(BaseProvider):
    provider_name = "Google"

    async def complete(self, prompt: str, system: str = "") -> ProviderResponse:
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(
            model_name=self.model_id,
            system_instruction=system or "You are a helpful assistant.",
        )
        start = time.monotonic()
        try:
            response = await model.generate_content_async(prompt)
            latency = int((time.monotonic() - start) * 1000)
            return ProviderResponse(
                model_id=self.model_id,
                content=response.text,
                latency_ms=latency,
                tokens_used=response.usage_metadata.total_token_count,
            )
        except Exception as e:
            return ProviderResponse(
                model_id=self.model_id, content="",
                latency_ms=0, error=str(e)
            )
