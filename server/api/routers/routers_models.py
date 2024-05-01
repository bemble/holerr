from pydantic import BaseModel

from typing import Optional
from datetime import datetime


# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------
class Constants(BaseModel):
    download_status: dict[str, int]
    torrent_status: dict[str, str]


# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
class InputPreset(BaseModel):
    pass


class InputRealDebrid(BaseModel):
    pass


class InputDebrider(BaseModel):
    pass


class InputSynologyDownloadStation(BaseModel):
    endpoint: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class InputDownloader(BaseModel):
    synology_download_station: Optional[InputSynologyDownloadStation] = None


class InputConfig(BaseModel):
    debug: list[str] = None
    debrider: Optional[InputDebrider] = None
    downloader: Optional[InputDownloader] = None
    presets: list[InputPreset] = None


# ------------------------------------------------------------
# DOWNLOADS
# ------------------------------------------------------------
class Download(BaseModel):
    id: str
    magnet: str
    title: str
    preset: str
    status: int
    total_bytes: int
    total_progress: int
    created_at: datetime
    updated_at: datetime
