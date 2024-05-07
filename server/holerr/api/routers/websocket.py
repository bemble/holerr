from holerr.core.websockets import manager
from holerr.core import config

from typing import Annotated
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException, status, Query, Depends

router = APIRouter(prefix="/ws")

async def check_api_key(
    websocket: WebSocket,
    x_api_key: Annotated[str | None, Query()] = None,
):
    api_key = config.api_key.get_secret_value()
    if not (api_key == "" or x_api_key == api_key):
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return x_api_key

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket, x_api_key: Annotated[str, Depends(check_api_key)]):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
