from server.core.db import db
from server.database.repositories import DownloadRepository

from fastapi import APIRouter

router = APIRouter(prefix="/actions")


@router.post("/clean_downloaded", response_model=list[str], tags=["Actions"])
async def clean_downloaded():
    session = db.new_session()
    return DownloadRepository(session).clean_downloaded()
