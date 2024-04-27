from torf import Torrent as TorfTorrent

from server.core.log import Log

log = Log.get_logger(__name__)


def get_hash(path: str) -> str:
    torrent = TorfTorrent.read(path)
    return torrent.infohash_base32


def get_name(path: str) -> str:
    torrent = TorfTorrent.read(path)
    return torrent.metainfo["info"]["name"]


def get_magnet_link(path: str) -> str:
    torrent = TorfTorrent.read(path)
    return str(torrent.magnet())
