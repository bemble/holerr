from holerr.core import config

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def check_api_key(api_key_header: str = Security(api_key_header)):
    api_key = config.api_key.get_secret_value()
    if not (api_key == "" or api_key_header == api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key",
        )
