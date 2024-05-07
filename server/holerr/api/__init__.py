from holerr.core import config
from .server import Server
from .routers import api_router

from fastapi import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles

server = Server()
server.app.include_router(api_router)

# Serve the frontend
# https://stackoverflow.com/a/73552966
class SpaStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except (HTTPException, StarletteHTTPException) as ex:
            if ex.status_code == 404:
                return await super().get_response("index.html", scope)
            else:
                raise ex
server.app.mount("", SpaStaticFiles(directory=config.public_dir, check_dir=False, html = True), name="Front")