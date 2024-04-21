from pydantic import BaseModel

TorrentStatus = {
    "MAGNET_ERROR": "magnet_error",
    "MAGNET_CONVERSION": "magnet_conversion",
    "WAITING_FILES_SELECTION": "waiting_files_selection",
    "QUEUED": "queued",
    "DOWNLOADING": "downloading",
    "DOWNLOADED": "downloaded",
    "ERROR": "error",
    "VIRUS": "virus",
    "COMPRESSING": "compressing",
    "UPLOADING": "uploading",
    "DEAD": "dead",
}


class File(BaseModel):
    id: int
    path: str  # Path to the file inside the torrent, starting with "/"
    bytes: int
    selected: int  # 0 or 1


class TorrentInfo(BaseModel):
    id: str
    filename: str
    bytes: int  # Size of selected files only
    progress: int  # Possible values: 0 to 100
    status: str  # Current status of the torrent
    files: list[File]
    links: list[str]
