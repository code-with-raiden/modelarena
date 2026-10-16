"""
ModelArena — /evaluate routes
POST /evaluate  → run full evaluation, return scored results
GET  /evaluate/{job_id} → poll async job status
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.router import dispatch_parallel
from app.core.evaluator import evaluate_responses

router = APIRouter()

DEFAULT_CRITERIA = ["Accuracy", "Clarity", "Depth", "Conciseness"]


class EvalRequest(BaseModel):
    prompt: str = Field(..., min_length=3)
    models: list[str] = Field(..., min_items=1)
    criteria: list[str] = DEFAULT_CRITERIA
    api_keys: dict[str, str] = {}   # user-supplied keys
    system_prompt: str = ""


class EvalResponse(BaseModel):
    prompt: str
    evaluations: list[dict]
    winner: str
    comparison: str
    latencies: dict[str, int]


@router.post("/", response_model=EvalResponse)
async def run_evaluation(req: EvalRequest):
    # 1. Dispatch to all models in parallel
    responses = await dispatch_parallel(
        prompt=req.prompt,
        model_ids=req.models,
        api_keys=req.api_keys,
        system=req.system_prompt,
    )

    # 2. Filter out total failures
    valid = [r for r in responses if r.content]
    if not valid:
        raise HTTPException(status_code=502, detail="All model calls failed.")

    # 3. Run evaluation agent
    result = await evaluate_responses(
        prompt=req.prompt,
        responses=valid,
        criteria=req.criteria,
        api_key=req.api_keys.get("anthropic"),
    )

    return EvalResponse(
        prompt=req.prompt,
        evaluations=result.get("evaluations", []),
        winner=result.get("winner", ""),
        comparison=result.get("comparison", ""),
        latencies={r.model_id: r.latency_ms for r in responses},
    )
