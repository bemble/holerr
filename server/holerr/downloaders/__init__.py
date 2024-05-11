from holerr.core import config

class WrappedDownloader():
    def __init__(self) -> None:
        self.update()

    def update(self):
        if config.downloader.synology_download_station:
            from .synology_download_station import SynologyDownloadStation
            self._downloader = SynologyDownloadStation()
        elif config.downloader.aria2_jsonrpc:
            from .aria2_jsonrpc import Aria2JsonRpc
            self._downloader = Aria2JsonRpc()
        else:
            self._downloader = None

    def __getattr__(self, name):
        if self._downloader is None:
            raise Exception("No downloader found")
        return getattr(self._downloader, name)

downloader = WrappedDownloader()

