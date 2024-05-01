from server.core import config

from fastapi import APIRouter

router = APIRouter(prefix="/presets")


@router.get("/", tags=["Presets"])
async def list_presets():
    return config.presets
