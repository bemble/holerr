from ..task import Task
from holerr.core.log import Log
from holerr.core.db import db
from holerr.core.config_repositories import PresetRepository
from holerr.database.models import Download, DownloadStatus
from holerr.database.repositories import DownloadRepository
from holerr.downloaders import downloader
from holerr.database.repositories import (
    DebriderInfoRepository,
    DebriderFileRepository,
    DownloaderInfoRepository,
    DownloaderTaskRepository,
)
from holerr.debriders import debrider
from holerr.core.websockets import manager, Actions

from sqlalchemy.orm import Session

log = Log.get_logger(__name__)


class TransitionHanlder:
    def __init__(self, session: Session):
        self._db_session = session

    def handle_transition(self, download: Download):
        if download.status == DownloadStatus["TORRENT_FOUND"]:
            log.debug("Sending torrent " + str(download.id) + " to debrider")
            self._send_to_debrider(download)

        if download.status == DownloadStatus["DEBRIDER_DOWNLOADED"]:
            log.debug(f"Sending torrent {download.id} to downloader")
            self._send_to_downloader(download)

    def _send_to_debrider(self, download: Download):
        debrider_id = debrider.add_magnet(download.magnet)
        debrider_info = debrider.get_torrent_info(debrider_id)
        download.status = DownloadStatus["TORRENT_SENT_TO_DEBRIDER"]
        download.total_progress = 1
        DebriderInfoRepository(self._db_session).create_model_from_torrent_info(
            debrider_info, download
        )
        DebriderFileRepository(self._db_session).create_models_from_torrent_info(
            debrider_info, download
        )

    def _send_to_downloader(self, download: Download):
        preset = PresetRepository.get_preset(download.preset)
        downloader_task_repo = DownloaderTaskRepository(self._db_session)
        for link in download.debrider_links:
            if link.is_unrestricted:
                id = downloader.add_download(link.link, download.title, preset)
                status = DownloadStatus["DOWNLOADER_DOWNLOADING"]
                downloader_task_repo.create_model(
                    id=id, status=status, bytes_downloaded=0, download=download
                )
        download.status = DownloadStatus["DOWNLOADER_DOWNLOADING"]
        download.total_progress = 50
        DownloaderInfoRepository(self._db_session).create_model(
            download=download, progress=0
        )
        debrider.delete_torrent(download.debrider_info.id)


class TaskDownloadStateTransition(Task):
    async def run(self):
        self._db_session = db.new_scoped_session()
        for download in self.get_downloads():
            handler = TransitionHanlder(self._db_session)
            handler.handle_transition(download)
            await manager.broadcast(Actions["DOWNLOADS_UPDATE"], download)

        self._db_session.commit()
        self._db_session.remove()

    def get_downloads(self) -> list[Download]:
        rep = DownloadRepository(self._db_session)
        return rep.get_all_handled_by_download_state_transition()
