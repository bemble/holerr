from holerr.core import config
from holerr.utils import info
from holerr.core.log import Log

from fastapi import FastAPI
import uvicorn

log = Log.get_logger(__name__)


class Server:
    def __init__(self):
        root_path = "" if config.base_path is None else config.base_path
        self._app = FastAPI(title="Holerr", version=info.get_app_version(), root_path=root_path)

    def start(self, port: int = 8765):
        log.debug(f"Starting server on port {port}")
        uvicorn.run(self._app, host="0.0.0.0", port=port)

    @property
    def app(self):
        return self._app
