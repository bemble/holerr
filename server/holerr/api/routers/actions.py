from holerr.core.db import db
from holerr.database.repositories import DownloadRepository
from holerr.core.exceptions import NotFoundException
from .routers_models import Download, Magnet
from holerr.utils import torrent

from typing import Annotated
from fastapi import APIRouter, HTTPException, status, File, Form
import tempfile

router = APIRouter(prefix="/actions")


@router.post("/add_magnet", response_model=Download, tags=["Actions"])
async def add_magnet(magnet: Magnet):
    try:
        session = db.new_session()
        download = DownloadRepository(session).create_model_from_magnet(magnet.uri, magnet.preset)
        session.refresh(download)
        return download
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/add_torrent", tags=["Actions"])
async def add_torrent(file: Annotated[bytes, File()], preset: Annotated[str, Form()]):
    try:
        tmp_torrent = tempfile.NamedTemporaryFile()
        tmp_torrent.write(file)
        magnet_uri = torrent.get_magnet_link(tmp_torrent.name)
        tmp_torrent.close()
        session = db.new_session()
        download = DownloadRepository(session).create_model_from_magnet(magnet_uri, preset)
        session.refresh(download)
        return download
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/clean_downloaded", response_model=list[str], tags=["Actions"])
async def clean_downloaded():
    session = db.new_session()
    return DownloadRepository(session).clean_downloaded()
