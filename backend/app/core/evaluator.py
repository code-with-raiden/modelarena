"""
ModelArena — Evaluation Agent
Uses Claude to score model responses across user-defined criteria.
"""
import json
import anthropic
from app.providers import ProviderResponse
from app.config import settings


EVAL_SYSTEM = """You are an expert AI evaluation judge. You receive:
- The original user prompt
- Responses from multiple AI models

Score each response on each criterion from 1–10.
Return ONLY valid JSON, no markdown, no explanation outside the JSON.

JSON shape:
{
  "evaluations": [
    {
      "model_id": "...",
      "scores": {"Accuracy": 8, "Clarity": 7, ...},
      "overall": 7.5,
      "strength": "one sentence",
      "weakness": "one sentence",
      "verdict": "one sentence summary"
    }
  ],
  "winner": "model_id",
  "comparison": "2-sentence comparative insight"
}"""


async def evaluate_responses(
    prompt: str,
    responses: list[ProviderResponse],
    criteria: list[str],
    api_key: str | None = None,
) -> dict:
    """
    Sends all model responses to Claude for structured scoring.
    Returns parsed evaluation dict.
    """
    key = api_key or settings.ANTHROPIC_API_KEY
    client = anthropic.AsyncAnthropic(api_key=key)

    # Build the user message
    responses_text = "\n\n".join([
        f"### {r.model_id}\n{r.content or '[ERROR: ' + str(r.error) + ']'}"
        for r in responses
    ])

    user_msg = (
        f"**Original Prompt:** {prompt}\n\n"
        f"**Criteria to score:** {', '.join(criteria)}\n\n"
        f"**Model Responses:**\n{responses_text}"
    )

    msg = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=EVAL_SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    )

    raw = msg.content[0].text
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Strip accidental markdown fences
        clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
