# ⬡ ModelArena

**Universal AI Model Evaluation Platform**  
One key (OpenRouter) → 16+ models → scored results in seconds.

---

## 🚀 Quickest way to run — GitHub Codespaces (zero local setup)

1. Go to **[github.com/code-with-raiden/modelarena](https://github.com/code-with-raiden/modelarena)**
2. Click the green **`<> Code`** button
3. Click **`Codespaces`** tab → **`Create codespace on main`**
4. Wait ~2 min for setup to complete automatically
5. Add your OpenRouter key to the `.env` file that appears:
   ```
   OPENROUTER_API_KEY=sk-or-v1-...
   ```
6. Open a terminal and run:
   ```bash
   bash .devcontainer/launch.sh
   ```
7. Click the pop-up to open port **5173** in your browser — done! 🎉

Everything runs online. Edit code in the browser VS Code, save, and it hot-reloads.

---

## 🌐 Production URLs (after deploy)

| Service  | Platform | URL |
|----------|----------|-----|
| Backend  | Railway  | `https://modelarena-api.railway.app` |
| Frontend | Vercel   | `https://modelarena.vercel.app` |
| API Docs | Railway  | `https://modelarena-api.railway.app/docs` |

---

## Deploy Backend → Railway (free tier)

1. Go to [railway.app](https://railway.app) → **New Project**
2. Click **Deploy from GitHub repo** → select `code-with-raiden/modelarena`
3. Set root directory to `backend`
4. Railway auto-detects the Dockerfile and deploys
5. Add environment variables in Railway dashboard:
   ```
   OPENROUTER_API_KEY=sk-or-v1-...
   DATABASE_URL=<Railway provides this automatically with Postgres plugin>
   REDIS_URL=<Railway provides this with Redis plugin>
   SECRET_KEY=<generate a random string>
   ```
6. Add **Postgres** plugin + **Redis** plugin from Railway dashboard
7. Copy your Railway backend URL

## Deploy Frontend → Vercel (free tier)

1. Go to [vercel.com](https://vercel.com) → **Add New Project**
2. Import `code-with-raiden/modelarena` from GitHub
3. Set root directory to `frontend`
4. Add environment variable:
   ```
   VITE_API_BASE=https://your-backend.railway.app
   ```
5. Click Deploy — done in 30 seconds

---

## Project Structure

```
modelarena/
├── .devcontainer/          ← GitHub Codespaces config (online dev)
│   ├── devcontainer.json
│   ├── setup.sh            ← auto-runs on Codespace creation
│   └── launch.sh           ← starts both servers with one command
├── backend/
│   ├── app/
│   │   ├── main.py         ← FastAPI entry point
│   │   ├── config.py       ← settings from .env
│   │   ├── api/            ← REST routes
│   │   ├── core/           ← parallel router + eval agent
│   │   ├── providers/      ← OpenRouter, Anthropic, OpenAI, Groq, Google, Mistral
│   │   └── integrations/   ← Slack bot
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── railway.toml        ← Railway deploy config
│   └── Procfile
├── frontend/
│   ├── src/
│   │   ├── pages/          ← EvalPage, HistoryPage
│   │   ├── components/     ← ModelSelector, CriteriaSelector, ResultsGrid
│   │   └── api/client.js   ← axios → backend
│   ├── vite.config.js
│   └── vercel.json         ← Vercel deploy config
├── vscode-extension/       ← VS Code plugin
├── cli/main.py             ← Typer CLI
├── deploy/
│   └── docker-compose.yml  ← local postgres + redis
└── .env.example            ← copy to .env, fill in keys
```

---

## API Keys needed

Only **one key** is required to run everything:

| Key | Where to get | What it unlocks |
|-----|-------------|-----------------|
| `OPENROUTER_API_KEY` | [openrouter.ai/keys](https://openrouter.ai/keys) | All 16 models |

Optional (only if you want direct provider access without OpenRouter):

| Key | Provider |
|-----|----------|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |
| `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com) |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) |
| `GOOGLE_API_KEY` | [aistudio.google.com](https://aistudio.google.com) |

---

## Tech Stack

- **FastAPI** + **Uvicorn** — async Python backend
- **SQLAlchemy 2.0** + **PostgreSQL** — eval history
- **Redis** + **ARQ** — async job queue
- **React 18** + **Vite** — web dashboard
- **Recharts** — radar charts in results
- **OpenRouter** — unified access to 16+ models
- **Docker Compose** — local dev stack
- **GitHub Codespaces** — online development
- **Railway** + **Vercel** — production hosting
