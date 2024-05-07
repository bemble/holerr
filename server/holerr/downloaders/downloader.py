from abc import ABC, abstractmethod
from holerr.core.config_models import Preset


class Downloader(ABC):
    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def add_download(self, uri: str, title: str, preset: Preset) -> str:
        pass

    @abstractmethod
    # Returns a tuple of the status of the download and the size downloaded
    def get_task_status(self, id: str) -> tuple[str, int]:
        pass

    @abstractmethod
    def delete_download(self, id: str):
        pass
