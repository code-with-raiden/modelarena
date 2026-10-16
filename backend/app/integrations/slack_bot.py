"""
ModelArena — Slack Bot Integration
Slash command: /eval <your prompt>
Mounted on FastAPI at POST /slack/events
"""
import os
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from fastapi import APIRouter, Request

from app.core.router import dispatch_parallel
from app.core.evaluator import evaluate_responses
from app.providers import list_models

slack_app = AsyncApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

handler = AsyncSlackRequestHandler(slack_app)
router = APIRouter()

DEFAULT_MODELS = ["claude-haiku-5-5", "gpt-4o-mini", "llama-3.3-70b-versatile"]
DEFAULT_CRITERIA = ["Accuracy", "Clarity", "Depth"]


@slack_app.command("/eval")
async def handle_eval_command(ack, body, respond):
    await ack()
    prompt = body.get("text", "").strip()
    if not prompt:
        await respond("Usage: `/eval <your prompt>`")
        return

    await respond("⏳ Evaluating across models — give me a moment...")

    # Run eval (uses server-side keys for Slack users)
    api_keys = {
        "anthropic": os.environ.get("ANTHROPIC_API_KEY", ""),
        "openai":    os.environ.get("OPENAI_API_KEY", ""),
        "groq":      os.environ.get("GROQ_API_KEY", ""),
    }
    responses = await dispatch_parallel(prompt, DEFAULT_MODELS, api_keys)
    result = await evaluate_responses(prompt, [r for r in responses if r.content], DEFAULT_CRITERIA)

    # Build Slack Block Kit response
    blocks = _build_blocks(prompt, result)
    await respond(blocks=blocks, replace_original=True)


def _build_blocks(prompt: str, result: dict) -> list:
    evals = result.get("evaluations", [])
    winner = result.get("winner", "")
    comparison = result.get("comparison", "")

    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": "🏆 ModelArena Results"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*Prompt:* {prompt}"}},
        {"type": "divider"},
    ]

    for ev in sorted(evals, key=lambda x: x.get("overall", 0), reverse=True):
        mid = ev["model_id"]
        overall = ev.get("overall", 0)
        crown = "👑 " if mid == winner else ""
        scores_str = " · ".join(f"{k}: *{v}*" for k, v in ev.get("scores", {}).items())
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn",
                     "text": f"{crown}*{mid}* — Overall: *{overall}/10*\n{scores_str}\n_{ev.get('verdict', '')}_"}
        })

    blocks += [
        {"type": "divider"},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"💡 {comparison}"}},
    ]
    return blocks


@router.post("/slack/events")
async def slack_events(req: Request):
    return await handler.handle(req)
