from holerr.core.log import Log

from fastapi import FastAPI, status
import re

from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse
from starlette.types import Receive, Scope, Send

log = Log.get_logger(__name__)


class ApiKey():
    def __init__(self, app: FastAPI, api_key: str, public_paths: list[str] = [], private_paths: list[str] = []):
        self.app = app
        self._api_key = api_key
        self._public_paths = public_paths
        self._private_paths = private_paths

    async def __call__(self, scope: Scope, receive: Receive, send:Send):
        if self._api_key == "":
            await self.app(scope, receive, send)
            return

        if scope.get("type") not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        if len(self._public_paths) > 0 :
            for path in self._public_paths:
                if re.match(path, scope.get("path")):
                    await self.app(scope, receive, send)
                    return

        if len(self._private_paths) > 0 :
            is_private = False
            for path in self._private_paths:
                if re.match(path, scope.get("path")):
                    is_private = True
                    break
            if not is_private:
                await self.app(scope, receive, send)
                return

        log.debug(f"APiKey middleware called for {scope.get('type')}")
        conn = HTTPConnection(scope)
        if not self._is_http_valid(conn):
            response = JSONResponse({"detail": "Missing or invalid API key"}, status_code=status.HTTP_401_UNAUTHORIZED)
            return await response(scope, receive, send)

        await self.app(scope, receive, send)

    def _is_http_valid(self, conn: HTTPConnection):
        return conn.headers.get("x-api-key") == self._api_key or conn.query_params.get("x_api_key") == self._api_key

