from server.debriders import debrider
from server.downloaders import downloader

from fastapi import APIRouter

router = APIRouter(prefix="/status")


@router.get("/")
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
