"""
ModelArena — /evaluate routes
POST /evaluate/        → run full evaluation synchronously
GET  /evaluate/models  → list recommended models for quick eval
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.core.router import dispatch_parallel
from app.core.evaluator import evaluate_responses
from app.providers import DEFAULT_MODELS

router = APIRouter()

DEFAULT_CRITERIA = ["Accuracy", "Clarity", "Depth", "Conciseness"]


class EvalRequest(BaseModel):
    prompt: str = Field(..., min_length=3, description="The prompt to evaluate")
    models: list[str] = Field(default=DEFAULT_MODELS, description="Model IDs to test")
    criteria: list[str] = Field(default=DEFAULT_CRITERIA, description="Scoring criteria")
    api_keys: dict[str, str] = Field(default={}, description="Provider API keys")
    system_prompt: str = Field(default="", description="Optional system prompt override")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Explain recursion simply",
                "models": [
                    "anthropic/claude-3-haiku",
                    "openai/gpt-4o-mini",
                    "meta-llama/llama-3.3-70b-instruct"
                ],
                "criteria": ["Accuracy", "Clarity", "Depth"],
                "api_keys": {"openrouter": "sk-or-v1-..."},
            }
        }


class EvalResponse(BaseModel):
    prompt: str
    models_tested: int
    evaluations: list[dict]
    winner: str
    runner_up: str
    comparison: str
    latencies_ms: dict[str, int]


@router.post("/", response_model=EvalResponse, summary="Run evaluation across models")
async def run_evaluation(req: EvalRequest):
    # 1. Dispatch all models in parallel
    responses = await dispatch_parallel(
        prompt=req.prompt,
        model_ids=req.models,
        api_keys=req.api_keys,
        system=req.system_prompt,
    )

    # 2. Filter models that completely failed
    valid = [r for r in responses if r.content]
    if not valid:
        raise HTTPException(status_code=502, detail="All model calls failed. Check your API keys.")

    # 3. Score with evaluation agent
    result = await evaluate_responses(
        prompt=req.prompt,
        responses=valid,
        criteria=req.criteria,
        openrouter_key=req.api_keys.get("openrouter"),
        anthropic_key=req.api_keys.get("anthropic"),
    )

    return EvalResponse(
        prompt=req.prompt,
        models_tested=len(valid),
        evaluations=result.get("evaluations", []),
        winner=result.get("winner", ""),
        runner_up=result.get("runner_up", ""),
        comparison=result.get("comparison", ""),
        latencies_ms={r.model_id: r.latency_ms for r in responses},
    )


@router.get("/models", summary="List default evaluation models")
async def get_default_models():
    return {"default_models": DEFAULT_MODELS}
