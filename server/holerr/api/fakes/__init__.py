from . import qbittorrent

from fastapi import APIRouter

fakes_router = APIRouter(prefix="/fake")
fakes_router.include_router(qbittorrent.router, prefix="/qbittorrent")
