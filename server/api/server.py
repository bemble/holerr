from server.core.log import Log

from fastapi import FastAPI
import uvicorn

log = Log.get_logger(__name__)


class Server:
    def __init__(self):
        self._app = FastAPI(title="Holerr")

    def start(self, port: int = 8765):
        log.debug(f"Starting server on port {port}")
        uvicorn.run(self._app, host="0.0.0.0", port=port)

    @property
    def app(self):
        return self._app
