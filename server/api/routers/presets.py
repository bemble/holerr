from server.core import config

from fastapi import APIRouter

router = APIRouter(prefix="/presets")


@router.get("/")
async def list():
    return config.presets
