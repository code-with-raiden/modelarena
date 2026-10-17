#!/bin/bash
set -e
echo "🚀 Setting up ModelArena dev environment..."

# ── Python backend ────────────────────────────────────────
echo "📦 Installing Python dependencies..."
cd /workspaces/modelarena/backend
pip install --quiet -r requirements.txt
echo "✅ Python deps installed"

# ── Node frontend ─────────────────────────────────────────
echo "📦 Installing Node dependencies..."
cd /workspaces/modelarena/frontend
npm install --silent
echo "✅ Node deps installed"

# ── Copy env template if .env doesn't exist ───────────────
cd /workspaces/modelarena
if [ ! -f .env ]; then
  cp .env.example .env
  echo "✅ .env created from template — add your OPENROUTER_API_KEY"
fi

# ── Start postgres + redis via Docker ─────────────────────
echo "🐳 Starting Postgres + Redis..."
cd /workspaces/modelarena/deploy
docker-compose up -d postgres redis
sleep 3
echo "✅ Postgres + Redis running"

echo ""
echo "══════════════════════════════════════════════════"
echo "  ModelArena is ready! Run these in two terminals:"
echo ""
echo "  Terminal 1 (backend):"
echo "    cd backend && uvicorn app.main:app --reload"
echo ""
echo "  Terminal 2 (frontend):"
echo "    cd frontend && npm run dev"
echo ""
echo "  Then open the browser preview on port 5173 🎉"
echo "══════════════════════════════════════════════════"
