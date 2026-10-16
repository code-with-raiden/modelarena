"""
ModelArena — /export routes (Phase 2: CSV / JSON export)
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def export_status():
    return {"message": "Export endpoints coming in Phase 2."}
