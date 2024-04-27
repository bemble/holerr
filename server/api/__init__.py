from .server import Server
from .routers import api_router

server = Server()
server.app.include_router(api_router)
