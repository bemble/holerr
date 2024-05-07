from holerr.core import config
from holerr.core.config_models import Config
from holerr.core.log import Log
from .routers_models import PartialConfig
from holerr.debriders import debrider
from holerr.downloaders import downloader

from fastapi import APIRouter

router = APIRouter(prefix="/configuration")

log = Log.get_logger(__name__)


@router.get("", response_model=Config, tags=["Configuration"])
async def get_configuration():
    return config.raw


@router.patch("", response_model=Config, tags=["Configuration"])
async def update_configuration(cfg: PartialConfig):
    update_data = cfg.model_dump(exclude_unset=True)
    config.update(update_data)
    debrider.update()
    downloader.update()

    return config.raw
