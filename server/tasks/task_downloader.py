from .task import Task
from server.core.log import Log
from server.core.db import db
from server.database.models import DownloadModel, DownloadStatus
from server.database.repositories import (
    DownloadRepository,
)
from server.downloaders import downloader
from server.downloaders.downloader_repositories import DownloaderRepository

log = Log.get_logger(__name__)


class DownloaderDownloadHanlder:
    def __init__(self, session):
        self._db_session = session

    def handle_download(self, download: DownloadModel):
        total_bytes_downloaded = 0
        for task in download.downloader_tasks:
            try:
                [status, size_downloaded] = downloader.get_task_status(task.id)
                task.status = DownloaderRepository.downloader_status_to_download_status(
                    status
                )
                task.bytes_downloaded = size_downloaded
                total_bytes_downloaded += size_downloaded
            except:
                task.status = DownloadStatus["ERROR_DOWNLOADER"]

        download_status = download.downloader_tasks[0].status
        for task in download.downloader_tasks:
            task_is_error = task.status == DownloadStatus["ERROR_DOWNLOADER"]
            download_is_error = download_status == DownloadStatus["ERROR_DOWNLOADER"]
            if (
                task.status < download_status or task_is_error
            ) and not download_is_error:
                download_status = task.status
        download.status = download_status
        download.downloader_info.progress = int(
            (total_bytes_downloaded * 100) / download.total_bytes
        )


class TaskDownloader(Task):
    async def run(self):
        self._db_session = db.new_scoped_session()
        for download in self.get_downloads():
            handler = DownloaderDownloadHanlder(self._db_session)
            handler.handle_download(download)

        self._db_session.commit()
        self._db_session.remove()

    def get_downloads(self) -> list[DownloadModel]:
        rep = DownloadRepository(self._db_session)
        return rep.get_all_handled_by_downloader()
