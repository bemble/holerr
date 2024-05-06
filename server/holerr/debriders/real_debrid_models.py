from typing import Optional
from pydantic import BaseModel
from .debrider_models import TorrentInfo as DebriderTorrentInfo


class Profile(BaseModel):
    id: int
    username: str
    email: str
    points: int  # Fidelity points
    locale: str  # User language
    avatar: str  # URL
    type: str  # "premium" or "free"
    premium: int  # seconds left as a Premium user
    expiration: str  # jsonDate


class ActiveCount(BaseModel):
    nb: int  # Number of currently active torrents
    limit: int  # Maximum number of active torrents you can have


class Torrent(BaseModel):
    id: str
    uri: str  # URL of the created ressource


class TorrentInfo(DebriderTorrentInfo):
    original_filename: str  # Original name of the torrent
    hash: str  # SHA1 Hash of the torrent
    original_bytes: int  # Total size of the torrent
    host: str  # Host main domain
    split: int  # Split size of links
    added: str  # jsonDate
    ended: Optional[str] = None  # Only present when finished, jsonDate
    speed: Optional[int] = (
        None  # Only present in "downloading", "compressing", "uploading" status
    )
    seeders: Optional[int] = (
        None  # Only present in "downloading", "magnet_conversion" status
    )


class UnrestrictedLink(BaseModel):
    id: str
    filename: str
    mimeType: str  # Mime Type of the file, guessed by the file extension
    filesize: int  # Filesize in bytes, 0 if unknown
    link: str  # Original link
    host: str  # Host main domain
    chunks: int  # Max Chunks allowed
    crc: int  # Disable / enable CRC check
    download: str  # Generated link
    streamable: int  # Is the file streamable on website
