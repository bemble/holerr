from ..task import Task
from holerr.core.log import Log
from holerr.core.db import db
from holerr.database.models import Download, DownloadStatus
from holerr.database.repositories import (
    DownloadRepository,
)
from holerr.downloaders import downloader
from holerr.downloaders.downloader_repositories import DownloaderRepository
from holerr.core.websockets import manager, Actions

log = Log.get_logger(__name__)


class DownloaderDownloadHanlder:
    def __init__(self, session):
        self._db_session = session

    def handle_download(self, download: Download):
        total_bytes_downloaded = 0
        for task in download.downloader_tasks:
            try:
                [status, size_downloaded] = downloader.get_task_status(task.id)
                task.status = DownloaderRepository.downloader_status_to_download_status(
                    status
                )
                task.bytes_downloaded = size_downloaded
                total_bytes_downloaded += size_downloaded
            except Exception:
                task.status = DownloadStatus["ERROR_DOWNLOADER"]

        download_status = download.downloader_tasks[0].status
        for task in download.downloader_tasks:
            task_is_error = task.status == DownloadStatus["ERROR_DOWNLOADER"]
            download_is_error = download_status == DownloadStatus["ERROR_DOWNLOADER"]
            if (
                task.status < download_status or task_is_error
            ) and not download_is_error:
                download_status = task.status

        download.downloader_info.progress = int(
            (total_bytes_downloaded * 100) / download.total_bytes
        )

        if download_status == DownloadStatus["DOWNLOADER_DOWNLOADED"]:
            download.status = DownloadStatus["DOWNLOADED"]
            download.total_progress = 100
        else:
            download.status = download_status
            download.total_progress = 50 + int(download.downloader_info.progress * 0.49)


class TaskDownloader(Task):
    async def run(self):
        self._db_session = db.new_scoped_session()
        for download in self.get_downloads():
            handler = DownloaderDownloadHanlder(self._db_session)
            before_hash = download.hash
            handler.handle_download(download)
            if before_hash != download.hash:
                log.debug("Hash changed, updating download")
                await manager.broadcast(Actions["DOWNLOADS_UPDATE"], download)

        self._db_session.commit()
        self._db_session.remove()

    def get_downloads(self) -> list[Download]:
        rep = DownloadRepository(self._db_session)
        return rep.get_all_handled_by_downloader()
