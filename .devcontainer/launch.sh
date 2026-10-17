#!/bin/bash
# One-command launcher — opens both servers in split terminals
# Usage: bash .devcontainer/launch.sh

SESSION="modelarena"

# Backend
echo "Starting FastAPI backend on :8000..."
cd /workspaces/modelarena/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

sleep 2

# Frontend
echo "Starting React frontend on :5173..."
cd /workspaces/modelarena/frontend
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!

echo ""
echo "✅ Backend PID: $BACKEND_PID  → http://localhost:8000"
echo "✅ Frontend PID: $FRONTEND_PID → http://localhost:5173"
echo "✅ API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

wait $BACKEND_PID $FRONTEND_PID
