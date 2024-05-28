from holerr.debriders import debrider
from holerr.downloaders import downloader
from .routers_models import Status
from holerr.utils import info
from holerr.tasks import worker

from fastapi import APIRouter

router = APIRouter(prefix="/status")


@router.get("", response_model=Status, tags=["Status"])
async def get_status():
    return {
        "app": {
            "version": info.get_app_version(),
            "worker": {
                "last_run": worker.last_run,
            }
        },
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
