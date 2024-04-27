from .server import Server
from .routers import constants

server = Server()
server.app.include_router(constants.router)
