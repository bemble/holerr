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
class PartialPreset(BaseModel):
    name: Optional[str] = None
    watch_dir: Optional[str] = None
    output_dir: Optional[str] = None
    create_sub_dir: Optional[bool] = None
    file_extensions: Optional[list[str]] = None
    min_file_size: Optional[str] = None


class PartialRealDebrid(BaseModel):
    api_key: Optional[str] = None


class PartialDebrider(BaseModel):
    real_debrid: Optional[PartialRealDebrid] = None


class PartialSynologyDownloadStation(BaseModel):
    endpoint: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class PartialDownloader(BaseModel):
    synology_download_station: Optional[PartialSynologyDownloadStation] = None


class PartialConfig(BaseModel):
    debug: list[str] = None
    debrider: Optional[PartialDebrider] = None
    downloader: Optional[PartialDownloader] = None
    presets: list[PartialPreset] = None


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


# ------------------------------------------------------------
# STATUS
# ------------------------------------------------------------
class StatusElement(BaseModel):
    id: str
    name: str
    connected: bool

class Status(BaseModel):
    debrider: StatusElement
    downloader: StatusElement