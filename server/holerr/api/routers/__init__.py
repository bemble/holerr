from ..fakes import qbittorrent
from . import actions, constants, config, downloads, presets, status, websocket

from fastapi import APIRouter, Depends

api_router = APIRouter(prefix="/api")
api_router.include_router(actions.router)
api_router.include_router(constants.router)
api_router.include_router(config.router)
api_router.include_router(downloads.router)
api_router.include_router(presets.router)
api_router.include_router(status.router)
api_router.include_router(websocket.router)

qbittorrent_router = APIRouter(prefix="/qbittorrent")
qbittorrent_router.include_router(qbittorrent.router)
