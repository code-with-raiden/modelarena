"""
ModelArena — /auth routes (Phase 2: JWT + API key vault)
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def auth_status():
    return {"message": "Auth coming in Phase 2 — currently use api_keys in request body."}
