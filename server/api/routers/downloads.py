from server.core.db import db
from .routers_models import Download
from server.database.repositories import DownloadRepository

from fastapi import APIRouter

router = APIRouter(prefix="/downloads")


@router.get("/", response_model=list[Download], tags=["Downloads"])
async def list_downloads():
    session = db.new_session()
    return DownloadRepository(session).get_all_models()
