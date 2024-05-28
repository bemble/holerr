from pydantic import BaseModel, SecretStr

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
    api_key: Optional[SecretStr] = None


class PartialDebrider(BaseModel):
    real_debrid: Optional[PartialRealDebrid] = None


class PartialSynologyDownloadStation(BaseModel):
    endpoint: Optional[str] = None
    username: Optional[str] = None
    password: Optional[SecretStr] = None

class PartialAria2JsonRpc(BaseModel):
    endpoint: Optional[str] = None
    secret: Optional[SecretStr] = None


class PartialDownloader(BaseModel):
    synology_download_station: Optional[PartialSynologyDownloadStation] = None
    aria2_jsonrpc: Optional[PartialAria2JsonRpc] = None


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
    to_delete: bool
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

class WorkerElement(BaseModel):
    last_run: datetime | None

class StatusApp(BaseModel):
    version: str
    worker: WorkerElement

class Status(BaseModel):
    app: StatusApp
    debrider: StatusElement
    downloader: StatusElement


# ------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------
class Magnet(BaseModel):
    uri: str
    preset: str