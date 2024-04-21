from abc import ABC, abstractmethod
from .debrider_models import TorrentInfo


class Debrider(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def get_slots_available(self) -> int:
        pass

    @abstractmethod
    def get_active_downloads(self):
        pass

    @abstractmethod
    def add_magnet(self, magnet: str) -> str:
        pass

    @abstractmethod
    def get_torrent_info(self, torrent_id: str) -> TorrentInfo:
        pass

    @abstractmethod
    def select_files(self, torrent_id: str, files: list[str]):
        pass

    @abstractmethod
    def delete_torrent(self, torrent_id: str):
        pass

    @abstractmethod
    def unrestricted_link(self, link: str) -> str | None:
        pass
