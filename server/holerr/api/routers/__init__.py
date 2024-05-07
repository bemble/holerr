from . import actions, constants, config, downloads, presets, status, websocket
from ..middlewares.api_key import check_api_key

from fastapi import APIRouter, Depends

api_router = APIRouter(prefix="/api")
api_router.include_router(actions.router, dependencies=[Depends(check_api_key)])
api_router.include_router(constants.router, dependencies=[Depends(check_api_key)])
api_router.include_router(config.router, dependencies=[Depends(check_api_key)])
api_router.include_router(downloads.router, dependencies=[Depends(check_api_key)])
api_router.include_router(presets.router, dependencies=[Depends(check_api_key)])
api_router.include_router(status.router, dependencies=[Depends(check_api_key)])
api_router.include_router(websocket.router)
