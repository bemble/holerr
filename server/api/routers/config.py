from server.core import config
from server.core.config_models import Config
from server.utils import secrets

from fastapi import APIRouter

router = APIRouter(prefix="/configuration")


def get_clean_conf():
    cfg = config.raw.copy()

    cfg.api_key = secrets.hide(cfg.api_key)

    if cfg.debrider.real_debrid:
        cfg.debrider.real_debrid.api_key = secrets.hide(
            cfg.debrider.real_debrid.api_key
        )

    if cfg.downloader.synology_download_station:
        cfg.downloader.synology_download_station.password = secrets.hide(
            cfg.downloader.synology_download_station.password
        )

    return cfg


@router.get("/", response_model=Config)
async def get_conf():
    return get_clean_conf()


@router.patch("/", response_model=Config)
async def update_conf(cfg: Config):
    update_data = cfg.dict(exclude_unset=True)
    config.raw = config.raw.copy(update=update_data)

    config.write()
    config.load()

    return get_clean_conf()
