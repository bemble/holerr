from holerr.core import config

class WrappedDownloader():
    def __init__(self) -> None:
        self.update()

    def update(self):
        if config.downloader.synology_download_station:
            from .synology_download_station import SynologyDownloadStation

            self._downloader = SynologyDownloadStation(config.downloader.synology_download_station)
        else:
            self._downloader = None

    def __getattr__(self, name):
        if self._downloader is None:
            raise Exception("No downloader found")
        return getattr(self._downloader, name)

downloader = WrappedDownloader()

