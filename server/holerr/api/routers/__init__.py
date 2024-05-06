from . import actions, constants, config, downloads, presets, status

from fastapi import APIRouter

api_router = APIRouter(prefix="/api")
api_router.include_router(actions.router)
api_router.include_router(constants.router)
api_router.include_router(config.router)
api_router.include_router(downloads.router)
api_router.include_router(presets.router)
api_router.include_router(status.router)
