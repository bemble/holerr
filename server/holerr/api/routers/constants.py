from .routers_models import Constants
from holerr.database.models import DownloadStatus
from holerr.debriders.debrider_models import TorrentStatus

from fastapi import APIRouter

router = APIRouter(prefix="/constants")


@router.get("", response_model=Constants, tags=["Constants"])
async def get_constants():
    return {"download_status": DownloadStatus, "torrent_status": TorrentStatus}
