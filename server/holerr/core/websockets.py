from fastapi import WebSocket
from typing import Any
from fastapi.encoders import jsonable_encoder

Actions = {
    "DOWNLOAD_NEW": "download/new",
    "DOWNLOAD_UPDATE": "download/update",
    "DOWNLOAD_DELETE": "download/delete"
}

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, action: str, payload: Any):
        for connection in self.active_connections:
            await connection.send_json({"action": action, "payload": jsonable_encoder(payload)})


manager = ConnectionManager()