from holerr.core import config
from .downloader import Downloader

downloader: Downloader | None = None

if config.downloader.synology_download_station:
    from .synology_download_station import SynologyDownloadStation

    downloader = SynologyDownloadStation(config.downloader.synology_download_station)

if downloader is None:
    raise Exception("No downloader found")
