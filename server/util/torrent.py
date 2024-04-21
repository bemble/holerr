import bencodepy
import hashlib
import base64


class Torrent:
    @staticmethod
    def _get_torrent_metadata(path: str) -> dict:
        return bencodepy.decode_from_file(path)[b"info"]

    @staticmethod
    def get_infohash(path: str) -> str:
        subj = Torrent._get_torrent_metadata(path)
        hashcontents = bencodepy.encode(subj)
        digest = hashlib.sha1(hashcontents).digest()
        b32hash = base64.b32encode(digest).decode()
        return b32hash

    @staticmethod
    def get_name(path: str) -> str:
        subj = Torrent._get_torrent_metadata(path)
        return subj[b"name"].decode()

    @staticmethod
    def get_magnet_link(path: str) -> str:
        metadata = Torrent._get_torrent_metadata(path)
        infohash = Torrent.get_infohash(path)
        dn = metadata[b"info"][b"name"].decode()
        tr = metadata[b"announce"].decode()
        xl = str(metadata[b"info"][b"length"], "utf-8")
        return f"magnet:?xt=urn:btih:{infohash}&dn={dn}&tr={tr}&xl={xl}"
