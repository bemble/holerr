from server.database.models import DownloadStatus
from server.debriders.debrider_models import TorrentStatus

from fastapi import APIRouter

router = APIRouter(prefix="/constants")


@router.get("/")
async def root():
    return {"download_status": DownloadStatus, "torrent_status": TorrentStatus}
