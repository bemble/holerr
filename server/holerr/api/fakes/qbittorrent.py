from holerr.core import config
from holerr.core.db import db
from holerr.core.config_repositories import PresetRepository
from holerr.database.repositories import DownloadRepository
from holerr.database.models import DownloadStatus
from .qbittorrent_models import Torrent
from .qbittorrent_repositories import QBittorrentTorrentRepository

import random
import string
from datetime import datetime

from fastapi import APIRouter, Request, Response, status, HTTPException
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/api/v2")


# Faked endpoints: https://github.com/Radarr/Radarr/blob/develop/src/NzbDrone.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs
# API documentation: https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1)

@router.get("/auth/login", tags=["QBittorrent"])
async def auth_login(response: Response):
    s = string.ascii_uppercase+string.ascii_lowercase+string.digits
    response.set_cookie(key="SID", value=f"{''.join(random.sample(s, 35))}", path="/")
    response.status_code = status.HTTP_200_OK
    return response

@router.get("/auth/logout", tags=["QBittorrent"])
async def auth_logout():
    return Response(status_code=status.HTTP_200_OK)


@router.get("/app/version", tags=["QBittorrent"])
async def app_version():
    return PlainTextResponse("v4.1.3")

@router.get("/app/webapiVersion", tags=["QBittorrent"])
async def app_webapiVersion():
    return PlainTextResponse("2.8.3")


@router.get("/app/preferences", tags=["QBittorrent"])
async def app_preferences():
    return {}

@router.get("/torrents/categories", tags=["QBittorrent"])
async def torrents_categories():
    categories = {}
    for preset in config.presets:
        categories[preset.name] = {"name":preset.name, "savePath":preset.output_dir}
    return categories

@router.get("/torrents/info", response_model=list[Torrent], tags=["QBittorrent"])
async def torrents_info(request:Request):
    preset_name = request.query_params.get("category")
    preset = PresetRepository().get_preset(preset_name)
    if preset is None:
        raise HTTPException(status_code=404, detail=f"Preset {preset_name} not found")
    session = db.new_session()
    downloads = DownloadRepository(session).get_all_for_preset(preset_name)

    response_torrents = []
    for download in downloads:
        torrent = QBittorrentTorrentRepository.torrent_from_download(download)
        response_torrents.append(torrent)
    return response_torrents
