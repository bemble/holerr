from pydantic import BaseModel, SecretStr

from typing import Optional
from datetime import datetime

TorrentState = {
    "ERROR" : "error",
    "DOWNLOADING": "downloading",
    "UPLOADING": "uploading"
}

class Torrent(BaseModel):
    hash: str
    name: str
    size: int
    progress: float
    eta: int
    state: str
    category: Optional[str] = None
    save_path: str
    content_path: str
    ratio: float
    last_activity: int