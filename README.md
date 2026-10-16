# ⬡ ModelArena

**Universal AI Model Evaluation Platform**  
One Python backend. Slack, VS Code, Teams, CLI, and REST API — all in one.

---

## Quick Start

```bash
# 1. Clone & setup
git clone https://github.com/you/modelarena
cd modelarena
cp .env.example .env          # fill in your API keys

# 2. Start services (postgres + redis + api)
cd deploy
docker-compose up -d

# 3. Test the API
curl -X POST http://localhost:8000/evaluate/ \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain recursion simply",
    "models": ["claude-haiku-5-5", "gpt-4o-mini"],
    "criteria": ["Accuracy", "Clarity"],
    "api_keys": {"anthropic": "sk-ant-...", "openai": "sk-..."}
  }'

# 4. Use the CLI
cd cli
pip install typer rich httpx
python main.py eval "Explain recursion" --models claude-haiku-5-5,gpt-4o-mini
```

---

## Project Structure

```
modelarena/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Settings (.env)
│   │   ├── api/                 # Route handlers
│   │   │   ├── routes_eval.py   # POST /evaluate
│   │   │   ├── routes_models.py # GET /models
│   │   │   ├── routes_auth.py   # Auth (Phase 2)
│   │   │   └── routes_export.py # CSV export (Phase 2)
│   │   ├── core/
│   │   │   ├── router.py        # Parallel model dispatch
│   │   │   └── evaluator.py     # Claude scoring agent
│   │   ├── providers/
│   │   │   ├── __init__.py      # Model registry + factory
│   │   │   ├── base.py          # Abstract BaseProvider
│   │   │   ├── anthropic.py
│   │   │   ├── openai.py
│   │   │   ├── groq.py
│   │   │   └── google.py
│   │   ├── integrations/
│   │   │   ├── slack_bot.py     # Slack /eval command
│   │   │   └── teams_bot.py     # MS Teams (Phase 2)
│   │   └── db/
│   │       └── session.py       # SQLAlchemy async
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                    # React dashboard (Phase 2)
├── vscode-extension/            # VS Code plugin
│   ├── extension.js
│   └── package.json
├── cli/
│   └── main.py                  # Typer CLI
├── deploy/
│   └── docker-compose.yml
├── .env.example
└── README.md
```

---

## API Reference

### `POST /evaluate/`
```json
{
  "prompt": "Your question here",
  "models": ["claude-haiku-5-5", "gpt-4o-mini", "llama-3.3-70b-versatile"],
  "criteria": ["Accuracy", "Clarity", "Depth", "Conciseness"],
  "api_keys": {
    "anthropic": "sk-ant-...",
    "openai": "sk-...",
    "groq": "gsk_..."
  }
}
```

### `GET /models/`
Returns all registered models and which API key they need.

---

## Integrations

| Surface       | Status   | How                                      |
|---------------|----------|------------------------------------------|
| REST API      | ✅ Ready  | POST /evaluate/ with your API keys       |
| CLI           | ✅ Ready  | `python cli/main.py eval "..."`          |
| Slack         | ✅ Ready  | `/eval <prompt>` slash command           |
| VS Code       | ✅ Ready  | Right-click selected text                |
| MS Teams      | 🔜 Phase2 | Bot Framework adaptive cards             |
| GitHub Action | 🔜 Phase2 | CI pipeline evaluation                   |
| Discord       | 🔜 Phase3 | `!eval` command                          |

---

## Adding a New Model
Edit `backend/app/providers/__init__.py`:
```python
MODEL_REGISTRY["new-model-id"] = (NewProvider, "api_key_name")
```
That's it — the new model appears in `/models/` and is available for evaluation.

---

## Tech Stack
- **FastAPI** + **Uvicorn** — async Python API server
- **SQLAlchemy 2.0 async** + **PostgreSQL** — eval history
- **Redis** + **ARQ** — job queue for long evaluations
- **anthropic / openai / groq / google-generativeai** — provider SDKs
- **slack-bolt** — Slack integration
- **Typer + Rich** — CLI
- **React + Vite** — web dashboard (Phase 2)
