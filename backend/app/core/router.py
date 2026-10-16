"""
ModelArena — Parallel Model Router
Dispatches a prompt to N models simultaneously using asyncio.gather().
"""
import asyncio
from app.providers import get_provider, ProviderResponse


async def dispatch_parallel(
    prompt: str,
    model_ids: list[str],
    api_keys: dict[str, str],
    system: str = "",
) -> list[ProviderResponse]:
    """
    Calls every model in parallel. Total time = slowest single model.
    Errors are captured per-model, never crash the whole evaluation.
    """
    async def call_one(model_id: str) -> ProviderResponse:
        try:
            provider = get_provider(model_id, api_keys)
            return await provider.complete(prompt, system=system)
        except Exception as e:
            return ProviderResponse(
                model_id=model_id, content="",
                latency_ms=0, error=str(e)
            )

    results = await asyncio.gather(*[call_one(m) for m in model_ids])
    return list(results)
