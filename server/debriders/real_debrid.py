from .debrider import Debrider
from server.core.config_models import RealDebrid as RealDebridConfig
from .real_debrid_models import (
    Profile,
    ActiveCount,
    Torrent,
    TorrentInfo,
    UnrestrictedLink,
)

import requests

ENDPOINT = "https://api.real-debrid.com/rest/1.0"
MAXIMUM_ACTIVE_DOWNLOADS = 20


class RealDebrid(Debrider):
    def __init__(self, conf: RealDebridConfig):
        self.api_key = conf.api_key

    def get_name(self) -> str:
        return "Real-Debrid"

    def is_connected(self) -> bool:
        try:
            if self._me() is not None:
                return True
        except Exception:
            pass
        return False

    def get_slots_available(self) -> int:
        return MAXIMUM_ACTIVE_DOWNLOADS - self._get_torrent_active_count().nb

    def get_active_downloads(self):
        # TODO
        pass

    def add_magnet(self, magnet: str) -> str:
        res = self._call("POST", "/torrents/addMagnet", data={"magnet": magnet})
        if res.status_code != 201:
            raise Exception(
                "Error while adding magnet, status code: " + str(res.status_code)
            )
        torrent_info = Torrent(**res.json())
        return torrent_info.id

    def get_torrent_info(self, torrent_id: str) -> TorrentInfo | None:
        res = self._call("GET", "/torrents/info/" + torrent_id)
        if res.status_code != 200:
            return None
        return TorrentInfo(**res.json())

    def select_files(self, torrent_id: str, files: list[str]):
        res = self._call(
            "POST",
            "/torrents/selectFiles/" + torrent_id,
            data={"files": ",".join(files)},
        )
        if res.status_code != 204:
            raise Exception(
                "Error while deleting torrent, status code: " + str(res.status_code)
            )

    def delete_torrent(self, torrent_id: str):
        res = self._call("DELETE", "/torrents/delete/" + torrent_id)
        if res.status_code != 204:
            raise Exception(
                "Error while deleting torrent, status code: " + str(res.status_code)
            )

    def unrestricted_link(self, link: str) -> str | None:
        return self._get_unrestricted_link(link).download

    def _call(self, method, path, **kwargs):
        if not kwargs.get("headers"):
            kwargs["headers"] = {}

        kwargs["headers"]["Authorization"] = "Bearer " + self.api_key
        return requests.request(method, ENDPOINT + path, **kwargs)

    def _me(self) -> Profile | None:
        res = self._call("GET", "/user")
        if res.status_code != 200:
            raise Exception("Error while getting user info")
        return Profile(**res.json())

    def _get_torrent_active_count(self) -> ActiveCount:
        res = self._call("GET", "/torrents/activeCount")
        if res.status_code != 200:
            raise Exception("Error while getting active count")
        return ActiveCount(**res.json())

    def _get_unrestricted_link(self, link: str) -> str:
        res = self._call("POST", "/unrestrict/link", data={"link": link})
        if res.status_code != 200:
            raise Exception("Error while unrestricting link")
        return UnrestrictedLink(**res.json())
