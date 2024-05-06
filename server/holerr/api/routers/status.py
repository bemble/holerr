from holerr.debriders import debrider
from holerr.downloaders import downloader
from .routers_models import Status

from fastapi import APIRouter

router = APIRouter(prefix="/status")


@router.get("", response_model=Status, tags=["Status"])
async def get_status():
    return {
        "debrider": {
            "id": debrider.get_id(),
            "name": debrider.get_name(),
            "connected": debrider.is_connected(),
        },
        "downloader": {
            "id": downloader.get_id(),
            "name": downloader.get_name(),
            "connected": downloader.is_connected(),
        },
    }
