from ..task import Task
from server.core.log import Log
from server.core.db import db
from server.core.config_repositories import PresetRepository
from server.database.models import DownloadModel, DownloadStatus
from server.database.repositories import (
    DownloadRepository,
    DebriderFileRepository,
    DebriderLinkRepository,
)
from server.debriders import debrider
from server.debriders.debrider_models import TorrentStatus, TorrentInfo
from server.debriders.debrider_repositories import FileRepository

from sqlalchemy.orm import Session

log = Log.get_logger(__name__)


class DebriderDownloadHanlder:
    def __init__(self, session: Session):
        self._db_session = session

    def handle_download(self, download: DownloadModel):
        debrider_info = debrider.get_torrent_info(download.debrider_info.id)

        if debrider_info == None:
            download.status = DownloadStatus["ERROR_DELETED_ON_DEBRIDER"]
            return

        download.debrider_info.status = debrider_info.status
        download.debrider_info.progress = debrider_info.progress

        if download.debrider_info.status == TorrentStatus["MAGNET_ERROR"]:
            log.debug("Magnet error " + str(download.id))
            download.status = DownloadStatus["ERROR_DEBRIDER"]

        if download.debrider_info.status == TorrentStatus["WAITING_FILES_SELECTION"]:
            self._on_waiting_file_selection(download)

        if download.debrider_info.status == TorrentStatus["DOWNLOADING"]:
            self._on_downloading(download)

        if download.debrider_info.status == TorrentStatus["DOWNLOADED"]:
            self._on_downloaded(download, debrider_info)

        if (
            download.debrider_info.status == TorrentStatus["COMPRESSING"]
            or download.debrider_info.status == TorrentStatus["UPLOADING"]
        ):
            self._on_post_download(download)

        if download.debrider_info.status == TorrentStatus["ERROR"]:
            log.debug("Debrider has torrent error " + download.id)
            download.status = DownloadStatus["ERROR_DEBRIDER"]

        if download.debrider_info.status == TorrentStatus["VIRUS"]:
            log.debug("Debrider found a virus " + download.id)
            download.status = DownloadStatus["ERROR_DEBRIDER"]

        if download.debrider_info.status == TorrentStatus["DEAD"]:
            log.debug("Debrider download is dead " + download.id)
            download.status = DownloadStatus["ERROR_DEBRIDER"]

    def _on_waiting_file_selection(self, download: DownloadModel):
        log.debug("Selecting files for " + str(download.id))
        preset = PresetRepository.get_preset(download.preset)
        preset_files = FileRepository.get_preset_files(download.debrider_files, preset)
        download.total_progress = 2
        if len(preset_files) == 0:
            log.debug("No file that match preset rules found " + download.id)
            download.status = DownloadStatus["ERROR_NO_FILES_FOUND"]
            return

        files = []
        download.total_bytes = 0
        for file in preset_files:
            files.append(str(DebriderFileRepository.get_torrent_file_id(file)))
            file.selected = True
            download.total_bytes += file.bytes
        debrider.select_files(download.debrider_info.id, files)
        download.total_progress = 3

    def _on_downloading(self, download: DownloadModel):
        if download.status != DownloadStatus["DEBRIDER_DOWNLOADING"]:
            download.status = DownloadStatus["DEBRIDER_DOWNLOADING"]
            log.debug("Debrider is downloading " + str(download.id))
        download.total_progress = 3 + int((download.debrider_info.progress) * 0.44)

    def _on_post_download(self, download: DownloadModel):
        log.debug("Debrider is doing post download actions " + str(download.id))
        download.status = DownloadStatus["DEBRIDER_POST_DOWNLOAD"]
        download.total_progress = 48

    def _on_downloaded(self, download: DownloadModel, debrider_info: TorrentInfo):
        log.debug("Debrider downloaded " + str(download.id))
        links_repo = DebriderLinkRepository(self._db_session)
        links_repo.create_models_from_torrent_info(debrider_info, download)
        unrestricted_links = []
        for link in debrider_info.links:
            unrestricted_link = debrider.unrestricted_link(link)
            unrestricted_links.append(unrestricted_link)
        links_repo.create_models(unrestricted_links, True, download)
        download.status = DownloadStatus["DEBRIDER_DOWNLOADED"]
        download.total_progress = 49


class TaskDebrider(Task):
    async def run(self):
        self._db_session = db.new_scoped_session()
        for download in self.get_downloads():
            handler = DebriderDownloadHanlder(self._db_session)
            handler.handle_download(download)

        self._db_session.commit()
        self._db_session.remove()

    def get_downloads(self) -> list[DownloadModel]:
        rep = DownloadRepository(self._db_session)
        return rep.get_all_handled_by_debrider()
