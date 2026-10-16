"""
ModelArena — FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import routes_eval, routes_models, routes_auth, routes_export
from app.db.session import init_db
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="ModelArena API",
    description="Universal AI model evaluation platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_auth.router,   prefix="/auth",     tags=["auth"])
app.include_router(routes_models.router, prefix="/models",   tags=["models"])
app.include_router(routes_eval.router,   prefix="/evaluate", tags=["evaluate"])
app.include_router(routes_export.router, prefix="/export",   tags=["export"])


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
