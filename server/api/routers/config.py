from server.core import config
from server.core.config_models import Config
from server.core.log import Log
from .routers_models import PartialConfig

from fastapi import APIRouter, status

router = APIRouter(prefix="/configuration")

log = Log.get_logger(__name__)


@router.get("/", response_model=Config, tags=["Configuration"])
async def get_configuration():
    return config.raw


@router.patch("/", response_model=Config, tags=["Configuration"])
async def update_configuration(cfg: PartialConfig):
    update_data = cfg.dict(exclude_unset=True)
    config.update(update_data)

    return config.raw
