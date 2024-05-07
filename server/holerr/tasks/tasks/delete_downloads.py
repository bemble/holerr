from ..task import Task
from holerr.core.log import Log
from holerr.core.db import db
from holerr.database.models import Download, DownloadStatus
from holerr.database.repositories import (
    DownloadRepository,
)
from holerr.debriders import debrider
from holerr.downloaders import downloader
from holerr.core.websockets import manager, Actions

from sqlalchemy.orm import Session

log = Log.get_logger(__name__)


class DeleteDownloadsdHanlder:
    def __init__(self, session: Session):
        self._db_session = session

    def handle_download(self, download: Download):
        if download.status == DownloadStatus["TORRENT_FOUND"]:
            # To early, torrent is added just after
            return

        if (
            download.status >= DownloadStatus["TORRENT_SENT_TO_DEBRIDER"]
            and download.status <= DownloadStatus["DEBRIDER_DOWNLOADED"]
        ):
            self._delete_debrider_download(download)

        if (
            download.status >= DownloadStatus["SENT_TO_DOWNLOADER"]
            and download.status <= DownloadStatus["DOWNLOADER_DOWNLOADED"]
        ):
            self._delete_downloader_download(download)
        self._db_session.delete(download)

    def _delete_debrider_download(self, download: Download):
        log.debug(f"Delete debrider download {download.debrider_info.id}")
        try:
            debrider.delete_torrent(download.debrider_info.id)
        except Exception as e:
            if (e.status_code == 404):
                log.debug(f"Debrider torrent {download.debrider_info.id} already deleted")
            else:
                raise e

    def _delete_downloader_download(self, download: Download):
        downloader_ids = [task.id for task in download.downloader_tasks]
        if len(downloader_ids) > 0:
            log.debug(f"Delete downloader downloads {','.join(downloader_ids)}")
            downloader.delete_download(",".join(downloader_ids))


class TaskDeleteDownloads(Task):
    async def run(self):
        self._db_session = db.new_scoped_session()
        for download in self.get_downloads():
            handler = DeleteDownloadsdHanlder(self._db_session)
            handler.handle_download(download)
            await manager.broadcast(Actions["DOWNLOADS_DELETE"], download)

        self._db_session.commit()
        self._db_session.remove()

    def get_downloads(self) -> list[Download]:
        rep = DownloadRepository(self._db_session)
        return rep.get_all_to_delete()
