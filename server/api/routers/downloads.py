from server.core.db import db
from server.database.repositories import DownloadRepository

from fastapi import APIRouter

router = APIRouter(prefix="/downloads")


@router.get("/")
async def list():
    session = db.new_session()
    return DownloadRepository(session).get_all_models()
