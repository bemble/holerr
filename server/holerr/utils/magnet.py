from torf import Magnet


def get_hash(magnet_uri: str) -> str:
    magnet = Magnet.from_string(magnet_uri)
    return magnet.infohash


def get_name(magnet_uri: str) -> str:
    magnet = Magnet.from_string(magnet_uri)
    return magnet.dn
