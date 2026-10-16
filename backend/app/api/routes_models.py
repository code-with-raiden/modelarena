"""
ModelArena — /models routes
GET /models → list all registered models
"""
from fastapi import APIRouter
from app.providers import list_models

router = APIRouter()


@router.get("/")
async def get_models():
    return {"models": list_models()}
