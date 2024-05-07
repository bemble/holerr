from torf import Torrent


def get_hash(path: str) -> str:
    torrent = Torrent.read(path)
    return torrent.infohash_base32


def get_name(path: str) -> str:
    torrent = Torrent.read(path)
    return torrent.metainfo["info"]["name"]


def get_magnet_link(path: str) -> str:
    torrent = Torrent.read(path)
    return str(torrent.magnet())
