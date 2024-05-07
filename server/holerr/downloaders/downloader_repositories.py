from .downloader_models import DownloadStatus
from holerr.database.models import DownloadStatus as DBDownloadStatus

StatusMapping: dict[str, int] = {}
StatusMapping[DownloadStatus["WAITING"]] = DBDownloadStatus["DOWNLOADER_DOWNLOADING"]
StatusMapping[DownloadStatus["DOWNLOADING"]] = DBDownloadStatus[
    "DOWNLOADER_DOWNLOADING"
]
StatusMapping[DownloadStatus["PAUSED"]] = DBDownloadStatus["DOWNLOADER_DOWNLOADING"]
StatusMapping[DownloadStatus["FINISHING"]] = DBDownloadStatus["DOWNLOADER_DOWNLOADING"]
StatusMapping[DownloadStatus["FINISHED"]] = DBDownloadStatus["DOWNLOADER_DOWNLOADED"]
StatusMapping[DownloadStatus["HASH_CHECKING"]] = DBDownloadStatus[
    "DOWNLOADER_DOWNLOADING"
]
StatusMapping[DownloadStatus["SEEDING"]] = DBDownloadStatus["DOWNLOADER_DOWNLOADED"]
StatusMapping[DownloadStatus["FILEHOSTING_WAITING"]] = DBDownloadStatus[
    "DOWNLOADER_DOWNLOADING"
]
StatusMapping[DownloadStatus["EXTRACTING"]] = DBDownloadStatus["DOWNLOADER_DOWNLOADING"]
StatusMapping[DownloadStatus["ERROR"]] = DBDownloadStatus["ERROR_DOWNLOADER"]


class DownloaderRepository:
    @staticmethod
    def downloader_status_to_download_status(status: str) -> int:
        return StatusMapping[status] or DBDownloadStatus["DOWNLOADER_DOWNLOADING"]
