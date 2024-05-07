from holerr.core.db import db
from .routers_models import Download
from holerr.database.repositories import DownloadRepository
from holerr.core.websockets import manager, Actions

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/downloads")


@router.get("", response_model=list[Download], tags=["Downloads"])
async def list_downloads():
    session = db.new_session()
    return DownloadRepository(session).get_all_models()


@router.delete("/{download_id}", response_model=Download, tags=["Downloads"])
async def delete_download(download_id: str):
    session = db.new_session()
    download = DownloadRepository(session).get_model(download_id)
    if download is None:
        raise HTTPException(status_code=404, detail=f"Download {download_id} not found")
    download.to_delete = True
    session.commit()
    session.refresh(download)

    await manager.broadcast(Actions["DOWNLOADS_UPDATE"], download)

    return download
