from .server import Server
from .middlewares import check_api_key
from .routers import api_router

from fastapi import Depends

server = Server()
server.app.include_router(api_router, dependencies=[Depends(check_api_key)])
