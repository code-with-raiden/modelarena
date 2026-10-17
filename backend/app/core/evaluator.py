"""
ModelArena — Evaluation Agent
Uses Claude (via OpenRouter or direct Anthropic) to score all model responses.
Supports any mix of criteria. Returns structured JSON.
"""
import json
import anthropic
from app.providers import ProviderResponse
from app.config import settings

EVAL_SYSTEM = """You are an expert AI model evaluation judge.

You receive a user prompt and responses from multiple AI models.
Score each response on each criterion from 1–10 (integers only).
Be fair, consistent, and realistic about each model's known strengths.

Return ONLY valid JSON — no markdown fences, no explanation outside the JSON.

Required shape:
{
  "evaluations": [
    {
      "model_id": "model/name",
      "scores": {"Accuracy": 8, "Clarity": 7, "Depth": 6},
      "overall": 7.0,
      "strength": "One sentence on what this model did best.",
      "weakness": "One sentence on where it fell short.",
      "verdict": "One sentence summary of this model's response quality."
    }
  ],
  "winner": "model/name of top scorer",
  "runner_up": "model/name of second place",
  "comparison": "2–3 sentence comparative insight across all models."
}"""


def _build_user_message(prompt: str, responses: list[ProviderResponse], criteria: list[str]) -> str:
    sections = []
    for r in responses:
        content = r.content if r.content else f"[FAILED — {r.error}]"
        sections.append(f"### {r.model_id}\n{content}")

    return (
        f"**User Prompt:** {prompt}\n\n"
        f"**Evaluation Criteria:** {', '.join(criteria)}\n\n"
        f"**Model Responses:**\n\n" + "\n\n---\n\n".join(sections)
    )


async def evaluate_responses(
    prompt: str,
    responses: list[ProviderResponse],
    criteria: list[str],
    openrouter_key: str | None = None,
    anthropic_key: str | None = None,
) -> dict:
    """
    Score all model responses using Claude as judge.
    Prefers OpenRouter key; falls back to direct Anthropic key.
    """
    # Resolve which key + base_url to use
    or_key = openrouter_key or settings.OPENROUTER_API_KEY
    ant_key = anthropic_key or settings.ANTHROPIC_API_KEY

    if or_key:
        client = anthropic.AsyncAnthropic(
            api_key=or_key,
            base_url="https://openrouter.ai/api/v1",
        )
        judge_model = "anthropic/claude-3.5-sonnet"
    elif ant_key:
        client = anthropic.AsyncAnthropic(api_key=ant_key)
        judge_model = "claude-sonnet-4-6"
    else:
        raise ValueError("No API key available for evaluation agent. Set OPENROUTER_API_KEY or ANTHROPIC_API_KEY.")

    user_msg = _build_user_message(prompt, responses, criteria)

    msg = await client.messages.create(
        model=judge_model,
        max_tokens=2048,
        system=EVAL_SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    )

    raw = msg.content[0].text.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
